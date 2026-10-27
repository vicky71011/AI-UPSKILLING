import os

from dotenv import load_dotenv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

load_dotenv(PROJECT_ROOT / ".env")

APP_NAME = os.getenv(
    "APP_NAME",
    "Ticket Intelligence",
)
APP_VERSION = os.getenv(
    "APP_VERSION",
    "0.1.0",
)
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

input_file = Path(
    os.getenv("DEFAULT_INPUT_FILE", "data/tickets.json")
)
DEFAULT_INPUT_FILE = (
    input_file if input_file.is_absolute()
    else PROJECT_ROOT / input_file
)