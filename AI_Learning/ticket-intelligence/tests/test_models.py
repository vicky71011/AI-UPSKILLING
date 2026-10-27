from datetime import datetime

from app.domain.ticket import Ticket

ticket = Ticket(
    ticket_id="INC001",
    description="Database connection timeout",
    priority="P2",
    status="OPEN",
    service="Database",
    created_by="siva",
    created_at=datetime(2026, 10, 5, 10, 0, 0),
)

print(ticket)
print(ticket.is_critical())
print(ticket.normalized_priority())
print(ticket.normalized_status())