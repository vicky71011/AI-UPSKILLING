import argparse

from pydantic import ValidationError

from app.exceptions.ticket_exceptions import TicketProcessingError
from app.services.ticket_service import TicketService
from app.utils.logging import get_logger
from config.settings import DEFAULT_INPUT_FILE


class ProcessTicket:
    def __init__(self):
        self.ticket_service = TicketService()
        self.logger = get_logger("process_tickets")

    def parse_arguments(self, argv=None):
        parser = argparse.ArgumentParser(
            description="Process and categorize support tickets"
        )
        parser.add_argument(
            "--input",
            dest="input_file",
            default=str(DEFAULT_INPUT_FILE),
            help="Path to the input JSON or CSV file",
        )
        return parser.parse_args(argv)

    def run(self, argv=None):
        try:
            args = self.parse_arguments(argv)

            self.logger.info(
                "Processing tickets from: %s",
                args.input_file,
            )

            results = self.ticket_service.process_file(args.input_file)

            self.logger.info(
                "Successfully processed %d tickets",
                len(results),
            )

            for ticket in results:
                print(f"\nTicket ID: {ticket.ticket_id}")
                print(f"Priority: {ticket.priority}")
                print(f"Status: {ticket.status}")
                print(f"Service: {ticket.service}")
                print(f"Category: {ticket.category}")
                print(f"Critical: {ticket.is_critical}")

            return 0

        except TicketProcessingError as exc:
            self.logger.error("Ticket processing failed: %s", exc)
            return 1

        except ValidationError as exc:
            self.logger.error("Ticket validation failed: %s", exc)
            return 1

        except Exception:
            self.logger.exception("An unexpected error occurred")
            return 1


def main():
    raise SystemExit(ProcessTicket().run())


if __name__ == "__main__":
    main()
