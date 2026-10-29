from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class TicketInput(BaseModel):
    ticket_id: str = Field(
        min_length=1,
        max_length=50,
        description="Unique identifier for the ticket",
    )
    description: str = Field(min_length=1, max_length=5000)
    priority: Literal["P1", "P2", "P3", "P4"] = Field(
        description="Ticket priority: P1, P2, P3, or P4",
    )
    status: Literal["OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"] = Field(default="OPEN")
    service: str = Field(min_length=1, max_length=100)
    created_by: str = Field(min_length=1, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("ticket_id", mode="before")
    @classmethod
    def validate_ticket_id(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("ticket_id cannot be empty")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("description cannot be empty")

        return value

    @field_validator("priority", mode="before")
    @classmethod
    def normalize_priority(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().upper()

        return value

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip().upper()

        return value

    @field_validator("service")
    @classmethod
    def validate_service(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("service cannot be empty")

        return value

    @field_validator("created_by")
    @classmethod
    def validate_created_by(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("created_by cannot be empty")

        return value


class TicketOutput(BaseModel):
    ticket_id: str
    description: str
    priority: str
    status: str
    service: str
    created_by: str
    created_at: datetime
    is_critical: bool
    category: str
    description_length: int
