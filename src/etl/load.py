"""
Load Service.
"""

import logging

from sqlalchemy import text

from src.database.database_service import DatabaseService


class LoadService:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.database = DatabaseService()

    # --------------------------------------------------
    # Bronze Layer
    # --------------------------------------------------

    def snapshot_exists(self, snapshot_date):

        sql = text("""
            SELECT COUNT(*)
            FROM bronze.crypto_market
            WHERE snapshot_date = :snapshot_date
        """)

        with self.database.engine.connect() as connection:

            result = connection.execute(
                sql,
                {"snapshot_date": snapshot_date}
            )

            return result.scalar() > 0

    def load_bronze(self, dataframe):

        self.database.load_dataframe(
            dataframe,
            table_name="crypto_market",
            schema="bronze"
        )

        self.logger.info("Bronze layer loaded successfully.")

    # --------------------------------------------------
    # Silver Layer
    # --------------------------------------------------

    def delete_silver_snapshot(self, snapshot_date):

        sql = text("""
            DELETE
            FROM silver.crypto_market_clean
            WHERE snapshot_date = :snapshot_date
        """)

        with self.database.engine.begin() as connection:

            connection.execute(
                sql,
                {"snapshot_date": snapshot_date}
            )

        self.logger.info(
            f"Deleted existing Silver snapshot: {snapshot_date}"
        )

    def load_silver(self, dataframe):

        with self.database.engine.begin() as connection:

            connection.execute(
                text("TRUNCATE TABLE silver.crypto_market_clean")
            )

        self.database.load_dataframe(
            dataframe,
            table_name="crypto_market_clean",
            schema="silver",
            if_exists="append"
        )

        self.logger.info("Silver layer loaded successfully.")

    # --------------------------------------------------
    # Warehouse Statistics
    # --------------------------------------------------

    def print_statistics(self):

        total_rows = self.database.total_rows()

        total_snapshots = self.database.total_snapshots()

        self.logger.info("=" * 60)
        self.logger.info("Warehouse Statistics")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Bronze Rows : {total_rows}")
        self.logger.info(f"Snapshots Stored  : {total_snapshots}")
        self.logger.info("=" * 60)