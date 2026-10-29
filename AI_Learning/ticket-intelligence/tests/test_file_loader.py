import json
from pathlib import Path

import pytest

from app.exceptions.ticket_exceptions import TicketProcessingError
from app.utils.file_loader import FileLoader

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def test_load_json():
    loader = FileLoader()

    records = loader.load(DATA_DIR / "tickets.json")

    assert isinstance(records, list)
    assert len(records) == 2
    assert isinstance(records[0], dict)
    assert records[0]["ticket_id"] == "INC001"


def test_load_csv():
    loader = FileLoader()

    records = loader.load(DATA_DIR / "tickets.csv")

    assert isinstance(records, list)
    assert len(records) == 2
    assert isinstance(records[0], dict)
    assert records[0]["ticket_id"] == "INC001"


def test_missing_file():
    loader = FileLoader()

    with pytest.raises(TicketProcessingError, match="File doesn't exist"):
        loader.load(DATA_DIR / "does_not_exist.json")


def test_unsupported_file(tmp_path):
    loader = FileLoader()
    unsupported_file = tmp_path / "tickets.txt"
    unsupported_file.write_text("some data", encoding="utf-8")

    with pytest.raises(TicketProcessingError, match="Unsupported file type"):
        loader.load(unsupported_file)


def test_invalid_json(tmp_path):
    loader = FileLoader()
    invalid_json_file = tmp_path / "invalid.json"
    invalid_json_file.write_text("{ invalid json", encoding="utf-8")

    with pytest.raises(TicketProcessingError, match="Invalid JSON file"):
        loader.load(invalid_json_file)


def test_json_root_is_not_list(tmp_path):
    loader = FileLoader()
    invalid_json_file = tmp_path / "object.json"
    invalid_json_file.write_text(
        json.dumps({"ticket_id": "INC001"}),
        encoding="utf-8",
    )

    with pytest.raises(
        TicketProcessingError,
        match="JSON file must contain a list of records",
    ):
        loader.load(invalid_json_file)


def test_json_record_is_not_dict(tmp_path):
    loader = FileLoader()
    invalid_json_file = tmp_path / "invalid_record.json"
    invalid_json_file.write_text(
        json.dumps(
            [
                {"ticket_id": "INC001"},
                "invalid record",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        TicketProcessingError,
        match="JSON file must contain a list of records",
    ):
        loader.load(invalid_json_file)


def test_uppercase_json_extension(tmp_path):
    loader = FileLoader()
    json_file = tmp_path / "tickets.JSON"
    json_file.write_text(
        json.dumps([{"ticket_id": "INC001"}]),
        encoding="utf-8",
    )

    records = loader.load(json_file)

    assert len(records) == 1
    assert records[0]["ticket_id"] == "INC001"


def test_directory_path_raises_error(tmp_path):
    loader = FileLoader()

    with pytest.raises(TicketProcessingError, match="Path is not a file"):
        loader.load(tmp_path)
