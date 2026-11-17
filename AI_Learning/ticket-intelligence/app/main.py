from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions.ticket_exceptions import TicketProcessingError
from app.models.ticket_models import TicketInput, TicketOutput
from app.services.ticket_service import TicketService

# Creates Instance of FastAPI application

app = FastAPI(
    title="Ticket Intelligence API",
    description="API for processing and categorizing support tickets",
    version="1.0.0",
)


def get_ticket_service() -> TicketService:
    return TicketService()


@app.exception_handler(TicketProcessingError)
async def handle_ticket_processing_error(
    _request: Request,
    _exc: TicketProcessingError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "TICKET_PROCESSING_ERROR",
            "detail": "An error occurred while processing the ticket.",
        },
    )


@app.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "application": "Ticket Intelligence",
    }


@app.post(
    "/tickets",
    response_model=TicketOutput,
    status_code=status.HTTP_200_OK,
)
def create_ticket(
    ticket: TicketInput, service: TicketService = Depends(get_ticket_service)
) -> TicketOutput:
    return service.process_ticket(ticket.model_dump())
