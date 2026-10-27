from pathlib import Path
import json
import csv

from app.exceptions.ticket_exceptions import TicketProcessingError

class FileLoader:

    def load(self, path: str | Path) -> list[dict]:

        if not isinstance(path, Path):
            path = Path(path)
    
        if not path.exists():
            raise TicketProcessingError(f"File doesn't exist: {path}")

        if path.suffix == ".json":
            return self.load_json(path)
        elif path.suffix == ".csv":
            return self.load_csv(path)
        else:
            raise TicketProcessingError(f"Unsupported file type: {path.suffix}")

    def load_json(self, path: Path) -> list[dict]:

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as e:
            raise TicketProcessingError(
                f"Invalid JSON file: {path}"
            ) from e

        if not isinstance(data, list):
            raise TicketProcessingError(
                f"JSON file must contain a list of records: {path}"
            )

        if not all(isinstance(record, dict) for record in data):
            raise TicketProcessingError(
                f"JSON file must contain a list of records: {path}"
            )

        return data

            

    def load_csv(self, path: Path) -> list[dict]:

        with path.open("r", encoding="utf-8") as file:
            data = list(csv.DictReader(file))

        return data