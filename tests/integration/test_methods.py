import os

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from tests.integration.const import DB_FOLDER, DB_PATH, BaseETLTest
from pipeline.const import TABLE_NAME


class TestETLPipelineMain(BaseETLTest):

    def test_init_method(self) -> None:
        """Testing method 'init'."""
        self.execute_and_validate(method="init")
        engine, inspector = self.get_engine_and_inspector()
        self.assertIn(
            TABLE_NAME,
            inspector.get_table_names(),
            f"Table {TABLE_NAME} was not created.",
        )

    def test_reset_method(self) -> None:
        """Testing method 'reset'."""
        if not os.path.exists(DB_FOLDER):
            os.makedirs(DB_FOLDER)
        with open(DB_PATH, "w") as f:
            f.write("Temporary DB content")

        self.execute_and_validate(method="reset", check_db_exists=False)

    def test_etl_method(self) -> None:
        """Testing method 'etl'. Making sure that the data have been uploaded"""
        self.execute_and_validate(method="init")
        self.execute_and_validate(method="etl")
        engine, inspector = self.get_engine_and_inspector()
        self.assertIn(
            TABLE_NAME,
            inspector.get_table_names(),
            f"Table {TABLE_NAME} was not created.",
        )

        Session = sessionmaker(bind=engine)
        with Session() as session:
            result = session.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
            row_count = result.scalar()
            self.assertGreater(row_count, 0, f"No data found in table '{TABLE_NAME}'.")

    def test_invalid_method(self) -> None:
        """Testing method 'invalid'."""
        result = self.run_command("invalid")
        self.assertNotEqual(
            result.returncode, 0, "Invalid method did not raise an error."
        )
        self.assertIn("Method invalid not recognized", result.stderr)
