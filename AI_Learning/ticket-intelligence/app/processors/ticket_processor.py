from app.models.ticket_models import TicketOutput
from app.domain.ticket import Ticket
from app.exceptions.ticket_exceptions import TicketProcessingError

class TicketProcessor:

    def process(self, ticket: Ticket) -> TicketOutput:
        if not isinstance(ticket, Ticket):
            raise TicketProcessingError("It is not a ticket format")

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

        if any(
            keyword in description 
            for keyword in ["database", "db", "sql"]
        ):
            return "DATABASE"
        elif any(
            keyword in description 
            for keyword in ['network', 'connection', 'timeout']
        ):          
            return "NETWORK"
        elif any(
            keyword in description 
            for keyword in ['server', 'cpu', 'memory']
        ):
            return "SERVER"
        elif any(
            keyword in description 
            for keyword in ['login', 'password', 'authentication']
        ):
            return "ACCESS"
        else:
            return "GENERAL"

    def calculate_description_length(self, description: str) -> int:
        return len(description)

   