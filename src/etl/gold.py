"""
Gold Layer Transformations.

Builds business-ready datasets from the Silver layer.

Creates:

1. market_summary
2. top10_coins
3. market_trends
"""

import logging

import pandas as pd
from sqlalchemy import text

from src.database.database_service import DatabaseService


class GoldService:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.database = DatabaseService()

    def build(self):

        self.logger.info("Reading Silver layer...")

        query = """
        SELECT *
        FROM silver.crypto_market_clean
        """

        dataframe = pd.read_sql(
            text(query),
            self.database.engine
        )

        self.logger.info(
            f"Retrieved {len(dataframe)} Silver records."
        )

        df = dataframe.copy()

        # -------------------------------------------------
        # Market Summary
        # -------------------------------------------------

        market_summary = (
            df.groupby("snapshot_date")
            .agg(
                total_market_cap=("market_cap", "sum"),
                average_price=("current_price", "mean"),
                average_24h_change=(
                    "price_change_percentage_24h",
                    "mean"
                ),
                total_volume=("total_volume", "sum"),
                total_coins=("coin_id", "count"),
                pipeline_timestamp=(
                    "pipeline_timestamp",
                    "max"
                )
            )
            .reset_index()
        )

        market_summary[
            [
                "total_market_cap",
                "average_price",
                "average_24h_change",
                "total_volume"
            ]
        ] = market_summary[
            [
                "total_market_cap",
                "average_price",
                "average_24h_change",
                "total_volume"
            ]
        ].round(2)

        self.logger.info(
            f"Market Summary created ({len(market_summary)} rows)"
        )

        # -------------------------------------------------
        # Top 10 Coins
        # -------------------------------------------------

        latest_snapshot = df["snapshot_date"].max()

        top10 = (
            df[df["snapshot_date"] == latest_snapshot]
            .sort_values(
                "market_cap",
                ascending=False
            )
            .head(10)
            .reset_index(drop=True)
        )

        self.logger.info(
            f"Top 10 dataset created ({len(top10)} rows)"
        )

        # -------------------------------------------------
        # Historical Market Trends
        # -------------------------------------------------

        market_trends = (
            df.sort_values(
                [
                    "snapshot_date",
                    "market_cap_rank"
                ]
            )
            .reset_index(drop=True)
        )

        self.logger.info(
            f"Market Trends created ({len(market_trends)} rows)"
        )

        self.logger.info(
            "Gold layer transformation completed."
        )

        return (
            market_summary,
            top10,
            market_trends
        )