"""
Silver Layer Transformations.

Reads data from Bronze,
cleans it,
and prepares the Silver layer.
"""

import logging

import pandas as pd
from sqlalchemy import text

from src.database.database_service import DatabaseService


class SilverService:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.database = DatabaseService()

    def build(self):

        self.logger.info("Reading Bronze layer...")

        query = """
        SELECT *
        FROM bronze.crypto_market
        """

        dataframe = pd.read_sql(
            text(query),
            self.database.engine
        )

        self.logger.info(
            f"Retrieved {len(dataframe)} Bronze records."
        )

        df = dataframe.copy()

        # ----------------------------------------
        # Remove duplicates
        # ----------------------------------------

        df = df.drop_duplicates(
            subset=["coin_id", "snapshot_date"]
        )

        # ----------------------------------------
        # Remove invalid values
        # ----------------------------------------

        df = df[df["current_price"] > 0]
        df = df[df["market_cap"] >= 0]
        df = df[df["total_volume"] >= 0]

        # ----------------------------------------
        # Standardise text
        # ----------------------------------------

        df["coin_name"] = df["coin_name"].str.title()
        df["symbol"] = df["symbol"].str.upper()

        # ----------------------------------------
        # Round numeric columns
        # ----------------------------------------

        numeric_cols = [
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_24h",
            "circulating_supply"
        ]

        df[numeric_cols] = df[numeric_cols].round(2)

        # ----------------------------------------
        # Keep only Silver columns
        # ----------------------------------------

        df = df[
            [
                "coin_id",
                "symbol",
                "coin_name",
                "current_price",
                "market_cap",
                "market_cap_rank",
                "total_volume",
                "price_change_percentage_24h",
                "circulating_supply",
                "snapshot_date",
                "pipeline_timestamp",
            ]
        ]

        # ----------------------------------------
        # Sort records
        # ----------------------------------------

        df = df.sort_values(
            ["snapshot_date", "market_cap"],
            ascending=[False, False]
        ).reset_index(drop=True)

        self.logger.info(
            f"Silver transformation complete ({len(df)} rows)"
        )

        return df