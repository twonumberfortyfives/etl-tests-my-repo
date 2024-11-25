from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FOLDER = BASE_DIR / "db"
DB_PATH = f"{DB_FOLDER}/applications.db"
CONN_STR = f"sqlite:///{DB_PATH}"
