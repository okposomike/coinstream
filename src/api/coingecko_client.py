"""
CoinGecko API Client.

Provides methods for interacting with the CoinGecko API.
"""

from src.api.base_client import BaseAPIClient
from src.config.settings import API_BASE_URL


class CoinGeckoClient(BaseAPIClient):
    """
    Client for the CoinGecko API.
    """

    def __init__(self):
        super().__init__()

    def get_market_data(
        self,
        vs_currency: str = "usd",
        order: str = "market_cap_desc",
        per_page: int = 100,
        page: int = 1,
        sparkline: bool = False,
        price_change_percentage: str = "24h"
    ):
        """
        Fetch cryptocurrency market data.

        Returns:
            List of cryptocurrencies.
        """

        endpoint = f"{API_BASE_URL}/coins/markets"

        params = {
            "vs_currency": vs_currency,
            "order": order,
            "per_page": per_page,
            "page": page,
            "sparkline": str(sparkline).lower(),
            "price_change_percentage": price_change_percentage
        }

        return self.get(endpoint, params=params)