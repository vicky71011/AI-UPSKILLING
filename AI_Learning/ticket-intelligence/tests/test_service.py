
from pathlib import Path

from app.exceptions.ticket_exceptions import TicketProcessingError
from app.models.ticket_models import TicketOutput
from app.services.ticket_service import TicketService


DATA_DIR = Path("data")


def sample_ticket() -> dict:
    return {
        "ticket_id": "INC101",
        "description": "Database connection timeout",
        "priority": "P1",
        "status": "OPEN",
        "service": "Database",
        "created_by": "siva",
        "created_at": "2026-10-05T10:00:00",
    }


def test_process_ticket():
    service = TicketService()

    result = service.process_ticket(sample_ticket())

    assert isinstance(result, TicketOutput)
    assert result.ticket_id == "INC101"
    assert result.priority == "P1"
    assert result.is_critical is True
    assert result.category == "DATABASE"
    assert result.description_length == len(
        "Database connection timeout"
    )

    print("Single ticket processing test passed!")


def test_process_file_json():
    service = TicketService()

    results = service.process_file(DATA_DIR / "tickets.json")

    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(item, TicketOutput) for item in results)
    assert results[0].ticket_id == "INC001"
    assert results[1].ticket_id == "INC002"

    print("JSON file processing test passed!")


def test_process_file_csv():
    service = TicketService()

    results = service.process_file(DATA_DIR / "tickets.csv")

    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(item, TicketOutput) for item in results)
    assert results[0].ticket_id == "INC001"
    assert results[1].ticket_id == "INC002"

    print("CSV file processing test passed!")


def test_invalid_ticket_data():
    service = TicketService()

    invalid_data = sample_ticket()
    invalid_data["priority"] = "P5"

    try:
        service.process_ticket(invalid_data)
        assert False, "Expected a validation error for priority P5"
    except ValueError as error:
        print(f"Invalid ticket validation test passed: {error}")


def test_process_file_missing_file():
    service = TicketService()

    try:
        service.process_file(DATA_DIR / "missing_tickets.json")
        assert False, "Expected TicketProcessingError for missing file"
    except TicketProcessingError as error:
        print(f"Missing file test passed: {error}")


if __name__ == "__main__":
    test_process_ticket()
    test_process_file_json()
    test_process_file_csv()
    test_invalid_ticket_data()
    test_process_file_missing_file()

    print("\nAll TicketService tests passed!")
