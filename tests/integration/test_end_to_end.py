import shutil
import sqlite3
import subprocess
import unittest
import os

from tests.integration.const import DB_FOLDER, DB_PATH


class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DB_FOLDER):
            shutil.rmtree(DB_FOLDER)

    def tearDown(self):
        if os.path.exists(DB_FOLDER):
            shutil.rmtree(DB_FOLDER)

    def test_full_pipeline(self):
        """E2E testing full process: reset → init → etl"""
        # Reset
        result = subprocess.run(
            ["python", "main.py", "--method", "reset"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Reset failed: {result.stderr}")

        # Init
        result = subprocess.run(
            ["python", "main.py", "--method", "init"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Init failed: {result.stderr}")
        self.assertTrue(os.path.exists(DB_PATH), "Database was not created.")

        # ETL
        result = subprocess.run(
            ["python", "main.py", "--method", "etl"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"ETL failed: {result.stderr}")
        self.assertIn("Data loaded to database succesfully", result.stdout)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vantaa_open_applications")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0, "ETL did not load data into the database.")
