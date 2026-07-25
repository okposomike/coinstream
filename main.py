"""
CoinStream Entry Point.
"""

import logging

from src.etl.extract import ExtractService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():

    extractor = ExtractService()

    filename, data = extractor.extract_market_data()

    print()

    print("=" * 60)

    print("CoinStream Extraction Successful")

    print("=" * 60)

    print(f"\nRecords Extracted : {len(data)}")

    print(f"Raw File Saved   : {filename}")

    print()


if __name__ == "__main__":
    main()