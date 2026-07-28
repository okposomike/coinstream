"""
Validation Service.

Responsible for:
- Checking missing values
- Removing duplicates
- Validating numeric columns
"""

import logging

import pandas as pd


class ValidationService:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

    def validate(self, df: pd.DataFrame):

        report = {}

        report["original_records"] = len(df)

        # Remove duplicate coins
        duplicates = df.duplicated(subset="coin_id").sum()

        df = df.drop_duplicates(subset="coin_id")

        report["duplicates_removed"] = duplicates

        # Count missing values
        report["missing_values"] = int(df.isnull().sum().sum())

        # Remove rows without a coin name
        df = df.dropna(subset=["coin_name"])

        # Validate numeric columns
        numeric_columns = [
            "current_price",
            "market_cap",
            "market_cap_rank",
            "total_volume",
            "high_24h",
            "low_24h",
            "price_change_percentage_24h",
            "circulating_supply"
        ]

        for column in numeric_columns:

            if column in df.columns:

                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        # Remove negative values
        df = df[df["current_price"] >= 0]
        df = df[df["market_cap"] >= 0]
        df = df[df["total_volume"] >= 0]

        report["validated_records"] = len(df)

        self.logger.info("Validation completed.")

        return df, report