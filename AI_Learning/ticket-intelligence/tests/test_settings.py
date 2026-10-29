import os
import subprocess
import sys
from pathlib import Path

from config.settings import (
    APP_NAME,
    APP_VERSION,
    DATA_DIR,
    DEFAULT_INPUT_FILE,
    LOG_LEVEL,
    PROJECT_ROOT,
)


def test_project_root():
    assert PROJECT_ROOT.is_absolute()
    assert PROJECT_ROOT.is_dir()
    assert (PROJECT_ROOT / "config" / "settings.py").is_file()


def test_data_directory():
    assert DATA_DIR == PROJECT_ROOT / "data"
    assert DATA_DIR.is_dir()


def test_application_settings():
    assert isinstance(APP_NAME, str)
    assert APP_NAME

    assert isinstance(APP_VERSION, str)
    assert APP_VERSION

    assert isinstance(LOG_LEVEL, str)
    assert LOG_LEVEL


def test_default_input_file():
    assert isinstance(DEFAULT_INPUT_FILE, Path)
    assert DEFAULT_INPUT_FILE.is_absolute()
    assert DEFAULT_INPUT_FILE.is_file()


def test_default_input_file_location():
    expected_path = PROJECT_ROOT / "data" / "tickets.json"
    assert DEFAULT_INPUT_FILE == expected_path


def test_custom_environment_settings(tmp_path):
    """Environment variables should override defaults in a fresh process."""
    env = os.environ.copy()
    env["APP_NAME"] = "Custom Ticket App"
    env["APP_VERSION"] = "2.0.0"
    env["LOG_LEVEL"] = "DEBUG"
    env["DEFAULT_INPUT_FILE"] = str(tmp_path / "custom.json")

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from config.settings import "
                "APP_NAME, APP_VERSION, LOG_LEVEL, DEFAULT_INPUT_FILE; "
                "print(APP_NAME); "
                "print(APP_VERSION); "
                "print(LOG_LEVEL); "
                "print(DEFAULT_INPUT_FILE)"
            ),
        ],
        cwd=PROJECT_ROOT,
        env={
            **env,
            "PYTHONPATH": (f"{PROJECT_ROOT}{os.pathsep}{PROJECT_ROOT / 'app'}"),
        },
        capture_output=True,
        text=True,
        timeout=10,
        check=True,
    )

    output = result.stdout.splitlines()

    assert output[0] == "Custom Ticket App"
    assert output[1] == "2.0.0"
    assert output[2] == "DEBUG"
    assert output[3] == str(tmp_path / "custom.json")
