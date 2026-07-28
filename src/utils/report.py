"""
Pipeline Reporting Utility.
"""

from datetime import datetime


class PipelineReport:

    @staticmethod
    def print(report):

        print()

        print("=" * 60)

        print("CoinStream Pipeline Report")

        print("=" * 60)

        print(f"Execution Time      : {datetime.now()}")

        print(f"Records Retrieved   : {report['original_records']}")

        print(f"Duplicates Removed  : {report['duplicates_removed']}")

        print(f"Missing Values      : {report['missing_values']}")

        print(f"Validated Records   : {report['validated_records']}")

        print()

        print("Pipeline Status     : SUCCESS")

        print("=" * 60)