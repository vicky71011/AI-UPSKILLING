from datetime import datetime

from app.domain.ticket import Ticket


def create_ticket(**overrides) -> Ticket:
    data = {
        "ticket_id": "INC001",
        "description": "Database connection timeout",
        "priority": "P2",
        "status": "OPEN",
        "service": "Database",
        "created_by": "siva",
        "created_at": datetime(2026, 10, 5, 10, 0, 0),
    }
    data.update(overrides)
    return Ticket(**data)


def test_ticket_creation():
    ticket = create_ticket()

    assert ticket.ticket_id == "INC001"
    assert ticket.description == "Database connection timeout"
    assert ticket.priority == "P2"
    assert ticket.status == "OPEN"


def test_ticket_is_critical():
    assert create_ticket(priority="P1").is_critical() is True
    assert create_ticket(priority="P2").is_critical() is False


def test_ticket_normalizes_priority_and_status():
    ticket = create_ticket(priority=" p2 ", status=" open ")

    assert ticket.priority == "P2"
    assert ticket.status == "OPEN"
    assert ticket.normalized_priority() == "P2"
    assert ticket.normalized_status() == "OPEN"


def test_ticket_strips_string_fields():
    ticket = create_ticket(
        ticket_id=" INC001 ",
        description=" Database connection timeout ",
        service=" Database ",
        created_by=" siva ",
    )

    assert ticket.ticket_id == "INC001"
    assert ticket.description == "Database connection timeout"
    assert ticket.service == "Database"
    assert ticket.created_by == "siva"


def test_ticket_rejects_empty_ticket_id():
    import pytest

    with pytest.raises(ValueError, match="ticket_id cannot be empty"):
        create_ticket(ticket_id="   ")


def test_ticket_rejects_invalid_priority():
    import pytest

    with pytest.raises(ValueError):
        create_ticket(priority="P5")
