class TicketException(Exception):
    pass

class InvalidTicketError(TicketException):
    pass

class TicketProcessingError(TicketException):
    pass