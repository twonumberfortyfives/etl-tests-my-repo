import os
import shutil
import subprocess
import unittest
from pathlib import Path

from sqlalchemy import create_engine, inspect

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FOLDER = BASE_DIR / "db"
DB_PATH = f"{DB_FOLDER}/applications.db"
CONN_STR = f"sqlite:///{DB_PATH}"


class BaseETLTest(unittest.TestCase):
    def setUp(self) -> None:
        """Setup shared cleanup logic for all test cases."""
        if os.path.exists(DB_FOLDER):
            shutil.rmtree(DB_FOLDER)
        os.makedirs(DB_FOLDER)

    def tearDown(self) -> None:
        """Cleanup logic after each test."""
        if os.path.exists(DB_FOLDER):
            shutil.rmtree(DB_FOLDER)

    @staticmethod
    def run_command(method: str) -> subprocess.CompletedProcess:
        """
        Runs the main.py script with the specified method and returns the result.
        """
        return subprocess.run(
            ["python", "main.py", "--method", method],
            capture_output=True,
            text=True,
        )

    def get_engine_and_inspector(self):
        engine = create_engine(CONN_STR)
        inspector = inspect(engine)
        return engine, inspector

    def execute_and_validate(self, method, check_db_exists=True) -> None:
        """
        Executes method and test the response
        :param method:
        :param check_db_exists:
        :return:
        """
        result = self.run_command(method)
        self.assertEqual(
            result.returncode, 0, f"{method.capitalize()} failed: {result.stderr}"
        )
        if check_db_exists:
            self.assertTrue(
                os.path.exists(DB_PATH),
                f"{method.capitalize()} did not create the database.",
            )
