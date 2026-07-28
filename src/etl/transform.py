"""
Transformation Service.

Responsible for:
- Validating raw data
- Selecting required columns
- Renaming columns
- Creating a clean DataFrame
"""

from datetime import datetime

import pandas as pd


class TransformService:

    def transform_market_data(self, raw_data):

        df = pd.DataFrame(raw_data)

        required_columns = [
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "market_cap_rank",
            "total_volume",
            "high_24h",
            "low_24h",
            "price_change_percentage_24h",
            "circulating_supply",
            "last_updated"
        ]

        df = df[required_columns]

        df = df.rename(
            columns={
                "id": "coin_id",
                "name": "coin_name"
            }
        )

        df["snapshot_date"] = datetime.now().date()

        df["pipeline_timestamp"] = datetime.now()

        return df