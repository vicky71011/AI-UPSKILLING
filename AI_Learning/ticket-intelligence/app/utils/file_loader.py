import csv
import json
from pathlib import Path

from app.exceptions.ticket_exceptions import TicketProcessingError


class FileLoader:
    def load(self, path: str | Path) -> list[dict]:

        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            raise TicketProcessingError(f"File doesn't exist: {path}")

        if not path.is_file():
            raise TicketProcessingError(f"Path is not a file: {path}")

        suffix = path.suffix.lower()

        if suffix == ".json":
            return self.load_json(path)
        elif suffix == ".csv":
            return self.load_csv(path)
        else:
            raise TicketProcessingError(f"Unsupported file type: {path.suffix}")

    def load_json(self, path: Path) -> list[dict]:

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            raise TicketProcessingError(f"Invalid JSON file: {path}") from exc
        except OSError as exc:
            raise TicketProcessingError(f"Unable to read JSON file: {path}") from exc

        if not isinstance(data, list) or not all(
            isinstance(record, dict) for record in data
        ):
            raise TicketProcessingError(
                f"JSON file must contain a list of records: {path}"
            )

        return data

    def load_csv(self, path: Path) -> list[dict]:
        try:
            with path.open("r", encoding="utf-8", newline="") as file:
                data = list(csv.DictReader(file))

        except (OSError, csv.Error) as exc:
            raise TicketProcessingError(f"Unable to read CSV file: {path}") from exc

        return data
