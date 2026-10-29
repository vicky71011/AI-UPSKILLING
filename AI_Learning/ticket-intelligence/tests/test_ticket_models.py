import pytest
from pydantic import ValidationError

from app.models.ticket_models import TicketInput


def test_valid_ticket():
    ticket = TicketInput(
        ticket_id=" INC001 ",
        description=" Database connection timeout ",
        priority=" p1 ",
        status=" in_progress ",
        service=" Database ",
        created_by=" siva ",
        created_at="2026-10-05T10:00:00",
    )

    assert ticket.ticket_id == "INC001"
    assert ticket.description == "Database connection timeout"
    assert ticket.priority == "P1"
    assert ticket.status == "IN_PROGRESS"
    assert ticket.service == "Database"
    assert ticket.created_by == "siva"
    assert ticket.created_at.year == 2026


def test_default_values():
    ticket = TicketInput(
        ticket_id="INC002",
        description="Server restarted",
        priority="P2",
        service="Server",
        created_by="admin",
    )

    assert ticket.status == "OPEN"
    assert ticket.created_at is not None


def test_invalid_ticket_id():
    with pytest.raises(ValidationError):
        TicketInput(
            ticket_id="   ",
            description="Database timeout",
            priority="P1",
            service="Database",
            created_by="siva",
        )


def test_invalid_priority():
    with pytest.raises(ValidationError):
        TicketInput(
            ticket_id="INC003",
            description="Database timeout",
            priority="P5",
            service="Database",
            created_by="siva",
        )


def test_invalid_status():
    with pytest.raises(ValidationError):
        TicketInput(
            ticket_id="INC004",
            description="Database timeout",
            priority="P2",
            status="UNKNOWN",
            service="Database",
            created_by="siva",
        )


def test_invalid_datetime():
    with pytest.raises(ValidationError):
        TicketInput(
            ticket_id="INC005",
            description="Database timeout",
            priority="P2",
            service="Database",
            created_by="siva",
            created_at="not-a-date",
        )
