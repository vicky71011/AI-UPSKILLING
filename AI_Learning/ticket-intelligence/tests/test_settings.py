
from pathlib import Path

from config.settings import (
    PROJECT_ROOT,
    DATA_DIR,
    APP_NAME,
    APP_VERSION,
    LOG_LEVEL,
    DEFAULT_INPUT_FILE,
)


def test_project_root():
    assert PROJECT_ROOT.is_absolute()
    assert PROJECT_ROOT.is_dir()
    assert (PROJECT_ROOT / "config" / "settings.py").is_file()

    print("Project root test passed!")


def test_data_directory():
    assert DATA_DIR == PROJECT_ROOT / "data"
    assert DATA_DIR.is_dir()

    print("Data directory test passed!")


def test_application_settings():
    assert isinstance(APP_NAME, str)
    assert APP_NAME == "Ticket Intelligence"

    assert isinstance(APP_VERSION, str)
    assert APP_VERSION == "0.1.0"

    assert isinstance(LOG_LEVEL, str)
    assert LOG_LEVEL == "INFO"

    print("Application settings test passed!")


def test_default_input_file():
    assert isinstance(DEFAULT_INPUT_FILE, Path)
    assert DEFAULT_INPUT_FILE.is_absolute()
    assert DEFAULT_INPUT_FILE.is_file()

    print("Default input file test passed!")


def test_default_input_file_location():
    expected_path = PROJECT_ROOT / "data" / "tickets.json"

    assert DEFAULT_INPUT_FILE == expected_path

    print("Default input file location test passed!")


if __name__ == "__main__":
    test_project_root()
    test_data_directory()
    test_application_settings()
    test_default_input_file()
    test_default_input_file_location()

    print("\nAll settings tests passed!")
