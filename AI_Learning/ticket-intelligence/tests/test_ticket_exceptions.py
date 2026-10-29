import pytest

from app.exceptions.ticket_exceptions import (
    InvalidTicketError,
    TicketException,
    TicketProcessingError,
)


@pytest.mark.parametrize(
    ("exception_class", "message"),
    [
        (InvalidTicketError, "Invalid ticket priority"),
        (TicketProcessingError, "Failed to process ticket"),
    ],
)
def test_exception_message(exception_class, message):
    error = exception_class(message)

    assert str(error) == message


def test_invalid_ticket_error_inherits_from_ticket_exception():
    assert issubclass(InvalidTicketError, TicketException)


def test_ticket_processing_error_inherits_from_ticket_exception():
    assert issubclass(TicketProcessingError, TicketException)


def test_ticket_exception_inherits_from_exception():
    assert issubclass(TicketException, Exception)


def test_ticket_exception_preserves_message():
    error = TicketException("Base ticket error")

    assert str(error) == "Base ticket error"
