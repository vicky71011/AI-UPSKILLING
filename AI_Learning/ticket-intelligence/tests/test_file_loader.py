from pathlib import Path
import json

from app.utils.file_loader import FileLoader
from app.exceptions.ticket_exceptions import TicketProcessingError


DATA_DIR = Path("data")


def test_load_json():
    loader = FileLoader()

    records = loader.load(DATA_DIR / "tickets.json")

    assert isinstance(records, list)
    assert len(records) == 2
    assert isinstance(records[0], dict)
    assert records[0]["ticket_id"] == "INC001"

    print("JSON loading test passed!")


def test_load_csv():
    loader = FileLoader()

    records = loader.load(DATA_DIR / "tickets.csv")

    assert isinstance(records, list)
    assert len(records) == 2
    assert isinstance(records[0], dict)
    assert records[0]["ticket_id"] == "INC001"

    print("CSV loading test passed!")


def test_missing_file():
    loader = FileLoader()

    try:
        loader.load(DATA_DIR / "does_not_exist.json")
        assert False, "Expected TicketProcessingError"
    except TicketProcessingError as e:
        print(f"Missing file test passed: {e}")


def test_unsupported_file():
    loader = FileLoader()

    unsupported_file = DATA_DIR / "tickets.txt"
    unsupported_file.write_text("some data", encoding="utf-8")

    try:
        loader.load(unsupported_file)
        assert False, "Expected TicketProcessingError"
    except TicketProcessingError as e:
        print(f"Unsupported file test passed: {e}")

    unsupported_file.unlink()


def test_invalid_json():
    loader = FileLoader()

    invalid_json_file = DATA_DIR / "invalid.json"
    invalid_json_file.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    try:
        loader.load(invalid_json_file)
        assert False, "Expected TicketProcessingError"
    except TicketProcessingError as e:
        print(f"Invalid JSON test passed: {e}")

    invalid_json_file.unlink()


def test_json_root_is_not_list():
    loader = FileLoader()

    invalid_json_file = DATA_DIR / "object.json"

    invalid_json_file.write_text(
        json.dumps({
            "ticket_id": "INC001"
        }),
        encoding="utf-8",
    )

    try:
        loader.load(invalid_json_file)
        assert False, "Expected TicketProcessingError"
    except TicketProcessingError as e:
        print(f"JSON root validation passed: {e}")

    invalid_json_file.unlink()


def test_json_record_is_not_dict():
    loader = FileLoader()

    invalid_json_file = DATA_DIR / "invalid_record.json"

    invalid_json_file.write_text(
        json.dumps([
            {
                "ticket_id": "INC001"
            },
            "invalid record",
        ]),
        encoding="utf-8",
    )

    try:
        loader.load(invalid_json_file)
        assert False, "Expected TicketProcessingError"
    except TicketProcessingError as e:
        print(f"JSON record validation passed: {e}")

    invalid_json_file.unlink()


if __name__ == "__main__":
    test_load_json()
    test_load_csv()
    test_missing_file()
    test_unsupported_file()
    test_invalid_json()
    test_json_root_is_not_list()
    test_json_record_is_not_dict()

    print("\nAll FileLoader tests passed!")