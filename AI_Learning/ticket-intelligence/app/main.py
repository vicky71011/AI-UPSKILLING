from fastapi import FastAPI
from fastapi import status

from app.models import TicketInput, TicketOutput
from app.services import TicketService

# Creates Instance of FastAPI application

app = FastAPI(
    title="Ticket Intelligence API",
    description="API for processing and categorizing support tickets",
    version="1.0.0",
)

ticket_service = TicketService()

@app.get('/')
def health_check():
    return {
        "status": "Healthy", 
        "application": "Ticket Intelligence",
    }

@app.post(
    '/tickets',
    response_model=TicketOutput,
    status_code=status.HTTP_200_OK,
)
def create_ticket(ticket: TicketInput):
    result = ticket_service.process_ticket(ticket.model_dump())
    
    return result