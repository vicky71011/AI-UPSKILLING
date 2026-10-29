from pathlib import Path

import pytest
from pydantic import ValidationError

from app.exceptions.ticket_exceptions import TicketProcessingError
from app.models.ticket_models import TicketOutput
from app.services.ticket_service import TicketService

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


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
    assert result.description_length == len("Database connection timeout")


def test_process_file_json():
    service = TicketService()

    results = service.process_file(DATA_DIR / "tickets.json")

    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(item, TicketOutput) for item in results)
    assert [item.ticket_id for item in results] == ["INC001", "INC002"]


def test_process_file_csv():
    service = TicketService()

    results = service.process_file(DATA_DIR / "tickets.csv")

    assert isinstance(results, list)
    assert len(results) == 2
    assert all(isinstance(item, TicketOutput) for item in results)
    assert [item.ticket_id for item in results] == ["INC001", "INC002"]


def test_invalid_ticket_data():
    service = TicketService()

    invalid_data = sample_ticket()
    invalid_data["priority"] = "P5"

    with pytest.raises(ValidationError):
        service.process_ticket(invalid_data)


def test_process_file_missing_file():
    service = TicketService()

    missing_file = DATA_DIR / "missing_tickets.json"

    with pytest.raises(TicketProcessingError, match="File doesn't exist"):
        service.process_file(missing_file)


def test_process_ticket_normalizes_input():
    service = TicketService()

    data = sample_ticket()
    data["ticket_id"] = " INC102 "
    data["priority"] = " p2 "
    data["status"] = " open "

    result = service.process_ticket(data)

    assert result.ticket_id == "INC102"
    assert result.priority == "P2"
    assert result.status == "OPEN"


def test_process_ticket_invalid_description():
    service = TicketService()

    data = sample_ticket()
    data["description"] = "   "

    with pytest.raises(ValidationError):
        service.process_ticket(data)


def test_process_file_unsupported_extension(tmp_path):
    service = TicketService()
    unsupported_file = tmp_path / "tickets.txt"
    unsupported_file.write_text("some data", encoding="utf-8")

    with pytest.raises(
        TicketProcessingError,
        match="Unsupported file type",
    ):
        service.process_file(unsupported_file)
