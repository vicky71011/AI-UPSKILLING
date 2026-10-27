import argparse
import logging
import sys

from services.ticket_service import TicketService
from utils.logging import get_logger
from config.settings import DEFAULT_INPUT_FILE

class ProcessTicket:
    def __init__(self):
        self.ticket_service = TicketService()
        self.logger = get_logger("process_tickets")

    def parse_arguments(self):
        parser = argparse.ArgumentParser(
            description="Process and categorize support tickets"
        )

        parser.add_argument(
            "--input",
            dest="input_file",
            default=str(DEFAULT_INPUT_FILE),
            help="Path to the input JSON or CSV file"
        )

        return parser.parse_args()

    def run(self):
        args = self.parse_arguments()

        self.logger.info("Processing tickets from: %s", args.input_file)

        results = self.ticket_service.process_file(args.input_file)

        self.logger.info("Successfully processed %d tickets", len(results))

        for ticket in results:
            print(f"\nTicket ID: {ticket.ticket_id}")
            print(f"Priority: {ticket.priority}")
            print(f"Category: {ticket.category}")
            print(f"Critical: {ticket.is_critical}")

if __name__ == "__main__":
    ProcessTicket().run()