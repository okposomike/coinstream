"""
Application configuration settings.
"""

API_BASE_URL = "https://api.coingecko.com/api/v3"

REQUEST_TIMEOUT = 30  # seconds

MAX_RETRIES = 3

BACKOFF_FACTOR = 2

USER_AGENT = "CoinStream/1.0"

DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json"
}