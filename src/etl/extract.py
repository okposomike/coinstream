"""
Extract Service.

Responsible for:
- Fetching raw data from CoinGecko
- Saving raw JSON snapshots
"""

import json
from datetime import datetime
from pathlib import Path

from src.api.coingecko_client import CoinGeckoClient


class ExtractService:
    """
    Handles extraction of raw cryptocurrency market data.
    """

    def __init__(self):

        self.client = CoinGeckoClient()

        self.raw_data_dir = Path("data/raw")

        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

    def extract_market_data(self):

        market_data = self.client.get_market_data()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = self.raw_data_dir / f"market_data_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as file:

            json.dump(
                market_data,
                file,
                indent=4
            )

        return filename, market_data