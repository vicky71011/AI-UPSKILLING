from pathlib import Path

from app.processors.ticket_processor import TicketProcessor
from app.utils.file_loader import FileLoader
from app.models.ticket_models import TicketInput, TicketOutput
from app.domain.ticket import Ticket

class TicketService:

    def __init__(self):
        self.file_loader = FileLoader()
        self.ticket_processor = TicketProcessor()

    def process_ticket(self, data: dict) -> TicketOutput:
        ticket_input = TicketInput(**data)
        validated_input = ticket_input.model_dump()

        ticket = Ticket(**validated_input)

        result = self.ticket_processor.process(ticket)        

        return result


    def process_file(self, path: str | Path) -> list[TicketOutput]:
        tikcets = self.file_loader.load(path)

        results = []

        for data in tikcets:
            ticket = self.process_ticket(data)
            results.append(ticket)
        
        return results