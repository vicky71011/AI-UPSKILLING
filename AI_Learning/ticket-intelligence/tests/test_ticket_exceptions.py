from app.exceptions.ticket_exceptions import (
    TicketException,
    InvalidTicketError,
    TicketProcessingError,
)

def test_invalid_ticket():
    try:
        raise InvalidTicketError("Invalid ticket priority")
    except InvalidTicketError as e:
        print("Caught:", e)

def test_processing_error():
    try:
        raise TicketProcessingError("Failed to process ticket")
    except TicketProcessingError as e:
        print("Caught:", e)

def test_base_exception():
    try:
        raise InvalidTicketError("Invalid ticket")
    except TicketException as e:
        print("Caught ticket exception:", e)

if __name__ == "__main__":
    test_invalid_ticket()
    test_processing_error()
    test_base_exception()