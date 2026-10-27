from dataclasses import dataclass
from datetime import datetime

@dataclass
class Ticket:

    ticket_id : str
    description : str
    priority : str
    status: str
    service : str
    created_by : str
    created_at : datetime

    def __post_init__(self):
        self.ticket_id = self.ticket_id.strip()
        self.description = self.description.strip()
        self.priority = self.normalized_priority()
        self.status = self.normalized_status()
        self.service = self.service.strip()
        self.created_by = self.created_by.strip()

        self._validate()

    def _validate(self) -> None:
        if not self.ticket_id:
            raise ValueError("Ticket cannot be empty!")

        if not self.description:
            raise ValueError("description cannot be empty")
        
        if self.priority not in {"P1", "P2", "P3", "P4"}:
            raise ValueError(
                f"Invalid priority: {self.priority}. "
                "Expected one of P1, P2, P3, P4."
            )

        if self.status not in {
            "OPEN", 
            "IN_PROGRESS",
            "RESOLVED",
            "CLOSED",
        }:
            raise ValueError(
                f"Invalid status: {self.status}. "
                "Expected one of OPEN, IN_PROGRESS, RESOLVED, CLOSED."
            )

        if not self.service:
            raise ValueError("service cannot be empty")

        if not self.created_by:
            raise ValueError("created_by cannot be empty")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime")

    def is_critical(self) -> bool:
        return self.priority == "P1"

    def normalized_priority(self) -> str:
        return self.priority.strip().upper()

    def normalized_status(self) -> str:
        return self.status.strip().upper()