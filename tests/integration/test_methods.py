import os
import shutil
import subprocess
import unittest

from tests.integration.const import DB_FOLDER, DB_PATH


class TestETLPipelineMain(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DB_FOLDER):
            shutil.rmtree(DB_FOLDER)

    def tearDown(self):
        if os.path.exists(DB_FOLDER):
            shutil.rmtree(DB_FOLDER)

    def test_init_method(self):
        """Testing method 'init'."""
        result = subprocess.run(
            ["python", "main.py", "--method", "init"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")
        self.assertTrue(os.path.exists(DB_PATH), "Database file was not created.")

    def test_reset_method(self):
        """Testing method 'reset'."""
        if not os.path.exists(DB_FOLDER):
            os.makedirs(DB_FOLDER)
        with open(DB_PATH, "w") as f:
            f.write("Temporary DB content")

        result = subprocess.run(
            ["python", "main.py", "--method", "reset"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")
        self.assertFalse(os.path.exists(DB_PATH), "Database file was not deleted.")

    def test_etl_method(self):
        """Testing method 'etl'."""
        subprocess.run(
            ["python", "main.py", "--method", "init"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertTrue(os.path.exists(DB_PATH), "Database has been created.")
        result = subprocess.run(
            ["python", "main.py", "--method", "etl"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Script failed: {result.stderr}")
        self.assertIn("Data loaded to database succesfully", result.stdout)

    def test_invalid_method(self):
        """Testing method 'invalid'."""
        result = subprocess.run(
            ["python", "main.py", "--method", "invalid"],
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0, "Invalid method did not raise an error.")
        self.assertIn("Method invalid not recognized", result.stderr)
