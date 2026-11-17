from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.exceptions.ticket_exceptions import TicketProcessingError
from app.main import app, get_ticket_service


def test_ticket_processing_error_returns_500():
    mock_service = Mock()

    mock_service.process_ticket.side_effect = TicketProcessingError(
        "Unable to process ticket"
    )

    def override_ticket_service():
        return mock_service

    app.dependency_overrides[get_ticket_service] = override_ticket_service

    try:
        client = TestClient(app)

        response = client.post(
            "/tickets",
            json={
                "ticket_id": "TEST001",
                "description": "Database connection failure",
                "priority": "P1",
                "status": "OPEN",
                "service": "database",
                "created_by": "admin",
            },
        )

        assert response.status_code == 500
        assert response.json() == {
            "error": "TICKET_PROCESSING_ERROR",
            "detail": "An error occurred while processing the ticket.",
        }

        mock_service.process_ticket.assert_called_once()

    finally:
        app.dependency_overrides.clear()