"""
CoinStream Pipeline.

Coordinates the complete ETL workflow.

CoinGecko API
        ↓
AWS S3
        ↓
Bronze Layer
        ↓
Silver Layer
"""

import logging

from src.etl.extract import ExtractService
from src.etl.transform import TransformService
from src.etl.validate import ValidationService
from src.etl.load import LoadService
from src.etl.silver import SilverService

from src.database.warehouse import WarehouseManager
from src.storage.s3_service import S3Service

from src.utils.report import PipelineReport


class CoinStreamPipeline:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.extractor = ExtractService()
        self.transformer = TransformService()
        self.validator = ValidationService()

        self.loader = LoadService()
        self.silver = SilverService()

        self.warehouse = WarehouseManager()

        self.s3 = S3Service()

    def run(self):

        try:

            self.logger.info("=" * 60)
            self.logger.info("CoinStream Pipeline Started")
            self.logger.info("=" * 60)

            # -----------------------------------------
            # Initialize Warehouse
            # -----------------------------------------

            self.warehouse.initialize()

            # -----------------------------------------
            # Extract
            # -----------------------------------------

            filename, raw_data = self.extractor.extract_market_data()

            # -----------------------------------------
            # Archive Raw JSON
            # -----------------------------------------

            self.logger.info("Uploading raw data to AWS S3...")

            s3_key = self.s3.upload_json(raw_data)

            self.logger.info(
                f"Raw data archived successfully: {s3_key}"
            )

            # -----------------------------------------
            # Transform
            # -----------------------------------------

            dataframe = self.transformer.transform_market_data(raw_data)

            # -----------------------------------------
            # Validate
            # -----------------------------------------

            dataframe, report = self.validator.validate(dataframe)

            snapshot_date = dataframe["snapshot_date"].iloc[0]

            # -----------------------------------------
            # Incremental Bronze
            # -----------------------------------------

            self.logger.info("Checking historical warehouse...")

            if not self.loader.snapshot_exists(snapshot_date):

                self.loader.load_bronze(dataframe)

            else:

                self.logger.info(
                    f"Snapshot {snapshot_date} already exists."
                )

                self.logger.info("Skipping Bronze load.")

            # -----------------------------------------
            # Build Silver Layer
            # -----------------------------------------

            self.logger.info("=" * 60)
            self.logger.info("Building Silver Layer")
            self.logger.info("=" * 60)

            silver_df = self.silver.build()

            self.loader.load_silver(silver_df)

            self.logger.info("Silver layer refreshed successfully.")

            # -----------------------------------------
            # Statistics
            # -----------------------------------------

            self.loader.print_statistics()

            # -----------------------------------------
            # Report
            # -----------------------------------------

            PipelineReport.print(report)

            self.logger.info("=" * 60)
            self.logger.info("CoinStream Pipeline Completed Successfully")
            self.logger.info("=" * 60)

            return dataframe

        except Exception as error:

            self.logger.exception(f"Pipeline Failed: {error}")

            raise