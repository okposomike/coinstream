"""
CoinStream Entry Point.
"""

import logging

from src.pipeline.pipeline import CoinStreamPipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():

    pipeline = CoinStreamPipeline()

    dataframe = pipeline.run()

    print("\n")

    print(dataframe.head())


if __name__ == "__main__":

    main()