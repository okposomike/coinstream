"""
Database Service.

Handles PostgreSQL connectivity,
schema creation,
table creation,
SQL execution,
and DataFrame loading.
"""

import logging
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from src.config.database import DATABASE_URL


class DatabaseService:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.engine = create_engine(DATABASE_URL)

    def test_connection(self):

        try:

            with self.engine.connect() as connection:

                connection.execute(text("SELECT 1"))

            self.logger.info("Database connection successful.")

            return True

        except SQLAlchemyError as error:

            self.logger.error(error)

            return False

    def execute_sql_file(self, file_path):

        sql = Path(file_path).read_text(encoding="utf-8")

        with self.engine.begin() as connection:

            connection.execute(text(sql))

        self.logger.info(f"Executed {file_path}")

    def load_dataframe(
        self,
        dataframe,
        table_name,
        schema,
        if_exists="append"
    ):

        dataframe.to_sql(
            table_name,
            self.engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            method="multi",
            chunksize=1000
        )

        self.logger.info(
            f"{len(dataframe)} records loaded into {schema}.{table_name}"
        )

    # ---------------------------------------------------
    # Historical Warehouse Functions
    # ---------------------------------------------------

    def snapshot_exists(self, snapshot_date):

        query = text("""
            SELECT COUNT(*)
            FROM bronze.crypto_market
            WHERE snapshot_date = :snapshot_date
        """)

        with self.engine.connect() as connection:

            count = connection.execute(
                query,
                {"snapshot_date": snapshot_date}
            ).scalar()

        return count > 0

    def total_rows(self):

        query = text("""
            SELECT COUNT(*)
            FROM bronze.crypto_market
        """)

        with self.engine.connect() as connection:

            total = connection.execute(query).scalar()

        return total

    def total_snapshots(self):

        query = text("""
            SELECT COUNT(DISTINCT snapshot_date)
            FROM bronze.crypto_market
        """)

        with self.engine.connect() as connection:

            total = connection.execute(query).scalar()

        return total