from datetime import datetime

import pytest

from app.domain.ticket import Ticket
from app.exceptions.ticket_exceptions import TicketProcessingError
from app.processors.ticket_processor import TicketProcessor


def create_ticket(
    description: str,
    priority: str = "P2",
) -> Ticket:
    return Ticket(
        ticket_id="INC001",
        description=description,
        priority=priority,
        status="OPEN",
        service="IT",
        created_by="siva",
        created_at=datetime(2026, 10, 5, 10, 0),
    )


def test_critical_ticket():
    processor = TicketProcessor()
    ticket = create_ticket(
        description="Database connection timeout",
        priority="P1",
    )

    result = processor.process(ticket)

    assert result.is_critical is True


def test_non_critical_ticket():
    processor = TicketProcessor()
    ticket = create_ticket(
        description="Database connection timeout",
        priority="P2",
    )

    result = processor.process(ticket)

    assert result.is_critical is False


def test_database_category():
    processor = TicketProcessor()
    ticket = create_ticket("Database connection timeout")

    result = processor.process(ticket)

    assert result.category == "DATABASE"


def test_network_category():
    processor = TicketProcessor()
    ticket = create_ticket("Network connection timeout")

    result = processor.process(ticket)

    assert result.category == "NETWORK"


def test_server_category():
    processor = TicketProcessor()
    ticket = create_ticket("Server CPU usage is very high")

    result = processor.process(ticket)

    assert result.category == "SERVER"


def test_access_category():
    processor = TicketProcessor()
    ticket = create_ticket("User login password authentication failed")

    result = processor.process(ticket)

    assert result.category == "ACCESS"


def test_general_category():
    processor = TicketProcessor()
    ticket = create_ticket("Printer is not working")

    result = processor.process(ticket)

    assert result.category == "GENERAL"


def test_description_length():
    processor = TicketProcessor()
    description = "Database timeout"
    ticket = create_ticket(description)

    result = processor.process(ticket)

    assert result.description_length == len(description)


def test_output_preserves_description():
    processor = TicketProcessor()
    description = "Database Connection Timeout"
    ticket = create_ticket(description)

    result = processor.process(ticket)

    assert result.description == description


def test_invalid_ticket_type():
    processor = TicketProcessor()

    with pytest.raises(
        TicketProcessingError,
        match="ticket must be an instance of Ticket",
    ):
        processor.process("not a ticket")


def test_database_keyword_uses_whole_word_matching():
    processor = TicketProcessor()

    assert processor.categorize("DB query failed") == "DATABASE"
    assert processor.categorize("SQL execution failed") == "DATABASE"
    assert processor.categorize("Debugging the application") == "GENERAL"


def test_category_precedence():
    processor = TicketProcessor()

    assert processor.categorize("Database server timeout") == "DATABASE"


def test_category_matching_is_case_insensitive():
    processor = TicketProcessor()

    assert processor.categorize("NETWORK CONNECTION FAILED") == "NETWORK"
    assert processor.categorize("database query failed") == "DATABASE"
