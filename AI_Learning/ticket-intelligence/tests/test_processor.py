from datetime import datetime

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

    print("\n--- Critical Ticket ---")
    print(result)

    assert result.is_critical is True


def test_database_category():
    processor = TicketProcessor()

    ticket = create_ticket(
        description="Database connection timeout"
    )

    result = processor.process(ticket)

    print("\n--- Database Category ---")
    print("Category:", result.category)

    assert result.category == "DATABASE"


def test_network_category():
    processor = TicketProcessor()

    ticket = create_ticket(
        description="Network connection timeout"
    )

    result = processor.process(ticket)

    print("\n--- Network Category ---")
    print("Category:", result.category)

    assert result.category == "NETWORK"


def test_server_category():
    processor = TicketProcessor()

    ticket = create_ticket(
        description="Server CPU usage is very high"
    )

    result = processor.process(ticket)

    print("\n--- Server Category ---")
    print("Category:", result.category)

    assert result.category == "SERVER"


def test_access_category():
    processor = TicketProcessor()

    ticket = create_ticket(
        description="User login password authentication failed"
    )

    result = processor.process(ticket)

    print("\n--- Access Category ---")
    print("Category:", result.category)

    assert result.category == "ACCESS"


def test_general_category():
    processor = TicketProcessor()

    ticket = create_ticket(
        description="Printer is not working"
    )

    result = processor.process(ticket)

    print("\n--- General Category ---")
    print("Category:", result.category)

    assert result.category == "GENERAL"


def test_description_length():
    processor = TicketProcessor()

    description = "Database timeout"

    ticket = create_ticket(
        description=description
    )

    result = processor.process(ticket)

    print("\n--- Description Length ---")
    print("Expected:", len(description))
    print("Actual:", result.description_length)

    assert result.description_length == len(description)


def test_output_preserves_description():
    processor = TicketProcessor()

    description = "Database Connection Timeout"

    ticket = create_ticket(
        description=description
    )

    result = processor.process(ticket)

    print("\n--- Description Preservation ---")
    print("Input:", description)
    print("Output:", result.description)

    assert result.description == description


def test_invalid_ticket_type():
    processor = TicketProcessor()

    try:
        processor.process("not a ticket")
    except TicketProcessingError as e:
        print("\n--- Invalid Ticket ---")
        print("Caught:", e)
    else:
        raise AssertionError(
            "TicketProcessingError was not raised"
        )


if __name__ == "__main__":
    test_critical_ticket()
    test_database_category()
    test_network_category()
    test_server_category()
    test_access_category()
    test_general_category()
    test_description_length()
    test_output_preserves_description()
    test_invalid_ticket_type()

    print("\nAll processor tests passed!")