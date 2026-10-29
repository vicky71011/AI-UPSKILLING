import re

from app.domain.ticket import Ticket
from app.exceptions.ticket_exceptions import TicketProcessingError
from app.models.ticket_models import TicketOutput


class TicketProcessor:
    def process(self, ticket: Ticket) -> TicketOutput:
        if not isinstance(ticket, Ticket):
            raise TicketProcessingError("ticket must be an instance of Ticket")

        ticket_output = TicketOutput(
            ticket_id=ticket.ticket_id,
            description=ticket.description,
            priority=ticket.priority,
            status=ticket.status,
            service=ticket.service,
            created_by=ticket.created_by,
            created_at=ticket.created_at,
            is_critical=ticket.is_critical(),
            category=self.categorize(ticket.description),
            description_length=self.calculate_description_length(ticket.description),
        )

        return ticket_output

    def categorize(self, description: str) -> str:
        description = description.lower()

        category_keywords = {
            "DATABASE": [r"database", r"db", r"sql"],
            "NETWORK": [r"network", r"connection", r"timeout"],
            "SERVER": [r"server", r"cpu", r"memory"],
            "ACCESS": [r"login", r"password", r"authentication"],
        }

        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if re.search(rf"\b{keyword}\b", description):
                    return category

        return "GENERAL"

    def calculate_description_length(self, description: str) -> int:
        return len(description)
