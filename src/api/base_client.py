"""
Reusable Base API Client.

This class handles:
- HTTP sessions
- GET requests
- Retry logic
- Timeout handling
- Logging
- Error handling

All API-specific clients (e.g. CoinGeckoClient)
should inherit from this class.
"""

import logging
import time
from typing import Any, Optional

import requests

from src.config.settings import (
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    BACKOFF_FACTOR,
    DEFAULT_HEADERS
)


class BaseAPIClient:
    """
    Base class for interacting with REST APIs.
    """

    def __init__(self):
        """
        Initialize HTTP session and logger.
        """

        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

        self.logger = logging.getLogger(__name__)

    def get(
        self,
        url: str,
        params: Optional[dict] = None
    ) -> Any:
        """
        Send a GET request with retry support.

        Args:
            url: API endpoint URL
            params: Query parameters

        Returns:
            Parsed JSON response

        Raises:
            requests.HTTPError
            requests.Timeout
            requests.RequestException
        """

        for attempt in range(1, MAX_RETRIES + 1):

            try:

                self.logger.info(
                    f"Attempt {attempt}: GET {url}"
                )

                response = self.session.get(
                    url=url,
                    params=params,
                    timeout=REQUEST_TIMEOUT
                )

                response.raise_for_status()

                self.logger.info(
                    f"Request successful ({response.status_code})"
                )

                return response.json()

            except requests.Timeout:

                self.logger.error(
                    f"Request timed out (Attempt {attempt})"
                )

            except requests.HTTPError as error:

                self.logger.error(
                    f"HTTP Error: {error}"
                )

                raise

            except requests.RequestException as error:

                self.logger.error(
                    f"Request failed: {error}"
                )

            if attempt < MAX_RETRIES:

                wait_time = BACKOFF_FACTOR ** attempt

                self.logger.info(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

        raise Exception(
            "Maximum retry attempts exceeded."
        )