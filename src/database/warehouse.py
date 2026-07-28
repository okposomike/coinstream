"""
Warehouse Manager.

Responsible for preparing the warehouse
before every pipeline execution.
"""

import logging

from src.database.database_service import DatabaseService


class WarehouseManager:

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self.database = DatabaseService()

    def initialize(self):

        self.logger.info("Initializing warehouse...")

        self.database.execute_sql_file("sql/create_tables.sql")

        self.logger.info("Warehouse ready.")