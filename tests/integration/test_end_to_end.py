from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from pipeline.const import TABLE_NAME
from tests.integration.const import BaseETLTest


class TestEndToEnd(BaseETLTest):
    def test_full_pipeline(self) -> None:
        """E2E testing full process: reset → init → etl"""
        # Reset
        self.execute_and_validate(method="reset", check_db_exists=False)

        # Init
        self.execute_and_validate(method="init")

        # ETL
        self.execute_and_validate(method="etl")

        engine, inspector = self.get_engine_and_inspector()

        Session = sessionmaker(bind=engine)
        with Session() as session:
            result = session.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
            row_count = result.scalar()
            self.assertGreater(row_count, 0, "ETL did not load data into the database.")
