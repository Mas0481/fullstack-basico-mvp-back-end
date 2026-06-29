import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "empresa.db"


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def configure(database_url=None, debug=None, log_level=None):
    """Permite sobrescrever configurações em testes ou scripts."""
    if database_url is not None:
        Config.DATABASE_URL = database_url
    if debug is not None:
        Config.DEBUG = debug
    if log_level is not None:
        Config.LOG_LEVEL = log_level.upper()
