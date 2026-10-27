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

    print("\n--- Valid Ticket ---")
    print(ticket)
    print("ticket_id:", ticket.ticket_id)
    print("priority:", ticket.priority)
    print("status:", ticket.status)
    print("created_at:", ticket.created_at)


def test_default_values():
    ticket = TicketInput(
        ticket_id="INC002",
        description="Server restarted",
        priority="P2",
        service="Server",
        created_by="admin",
    )

    print("\n--- Default Values ---")
    print("status:", ticket.status)
    print("created_at:", ticket.created_at)


def test_invalid_ticket_id():
    try:
        TicketInput(
            ticket_id="   ",
            description="Database timeout",
            priority="P1",
            service="Database",
            created_by="siva",
        )
    except ValidationError as e:
        print("\n--- Invalid Ticket ID ---")
        print(e)


def test_invalid_priority():
    try:
        TicketInput(
            ticket_id="INC003",
            description="Database timeout",
            priority="P5",
            service="Database",
            created_by="siva",
        )
    except ValidationError as e:
        print("\n--- Invalid Priority ---")
        print(e)


def test_invalid_status():
    try:
        TicketInput(
            ticket_id="INC004",
            description="Database timeout",
            priority="P2",
            status="UNKNOWN",
            service="Database",
            created_by="siva",
        )
    except ValidationError as e:
        print("\n--- Invalid Status ---")
        print(e)


def test_invalid_datetime():
    try:
        TicketInput(
            ticket_id="INC005",
            description="Database timeout",
            priority="P2",
            service="Database",
            created_by="siva",
            created_at="not-a-date",
        )
    except ValidationError as e:
        print("\n--- Invalid Datetime ---")
        print(e)


if __name__ == "__main__":
    test_valid_ticket()
    test_default_values()
    test_invalid_ticket_id()
    test_invalid_priority()
    test_invalid_status()
    test_invalid_datetime()