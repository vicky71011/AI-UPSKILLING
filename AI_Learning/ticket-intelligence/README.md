
# Ticket Intelligence

A Python application for validating, processing, and categorizing support tickets from JSON and CSV files.

## Overview

Ticket Intelligence is a modular Python application built to demonstrate clean code organization, data validation, exception handling, logging, command-line interfaces, and automated testing.

The application reads ticket records, validates their fields, converts them into domain objects, categorizes their descriptions using keyword-based rules, and produces structured output.

## Features

- **JSON and CSV support:** Load ticket records from either format.
- **Input validation:** Validate ticket fields using Pydantic.
- **Domain modeling:** Represent tickets using Python dataclasses.
- **Automatic categorization:** Categorize tickets based on description keywords.
- **Critical ticket detection:** Identify P1 priority tickets.
- **Structured logging:** Record processing progress and errors.
- **Command-line interface:** Specify an input file using `--input`.
- **Exception handling:** Handle file-processing and validation failures.
- **Automated testing:** Verify application behavior with pytest.

## Technology Stack

- Python 3.10+
- Pydantic 2
- python-dotenv
- pytest
- setuptools

## Project Structure

```text
ticket-intelligence/
├── app/
│   ├── domain/
│   │   └── ticket.py
│   ├── exceptions/
│   │   └── ticket_exceptions.py
│   ├── models/
│   │   └── ticket_models.py
│   ├── processors/
│   │   └── ticket_processor.py
│   ├── services/
│   │   └── ticket_service.py
│   ├── utils/
│   │   ├── file_loader.py
│   │   └── logging.py
│   ├── main.py
│   └── __init__.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── data/
│   ├── tickets.csv
│   └── tickets.json
├── scripts/
│   └── process_tickets.py
├── tests/
│   ├── test_file_loader.py
│   ├── test_logging.py
│   ├── test_process_tickets.py
│   ├── test_processor.py
│   ├── test_service.py
│   ├── test_settings.py
│   ├── test_ticket_exceptions.py
│   └── test_ticket_models.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10 or newer
- pip
- A terminal or command prompt

## Installation

### 1. Clone the repository

If you have the project in a Git repository:

```bash
git clone <repository-url>
cd ticket-intelligence
```

Alternatively, navigate to your existing project directory.

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on Linux or macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Running the Application

The command-line entry point is `scripts/process_tickets.py`.

Because the current project uses imports from both the `app` package and modules within `app/`, set the Python import path when running the script from the project root.

### Process a CSV file

```bash
PYTHONPATH=".:app" python scripts/process_tickets.py --input data/tickets.csv
```

### Process a JSON file

```bash
PYTHONPATH=".:app" python scripts/process_tickets.py --input data/tickets.json
```

### Use the default input file

The default input file is configured through `DEFAULT_INPUT_FILE` in `config/settings.py`.

```bash
PYTHONPATH=".:app" python scripts/process_tickets.py
```

### Display command-line help

```bash
PYTHONPATH=".:app" python scripts/process_tickets.py --help
```

## Ticket Data Format

Each ticket contains the following fields:

| Field | Description |
|---|---|
| `ticket_id` | Unique ticket identifier |
| `description` | Description of the reported issue |
| `priority` | Ticket priority: P1, P2, P3, or P4 |
| `status` | OPEN, IN_PROGRESS, RESOLVED, or CLOSED |
| `service` | Service associated with the ticket |
| `created_by` | Identifier of the ticket creator |
| `created_at` | Ticket creation date and time |

### Example JSON input

```json
[
  {
    "ticket_id": "INC001",
    "description": "Database connection timeout",
    "priority": "P1",
    "status": "OPEN",
    "service": "Database",
    "created_by": "user1",
    "created_at": "2026-10-28T10:00:00"
  },
  {
    "ticket_id": "INC002",
    "description": "Network connectivity issue",
    "priority": "P2",
    "status": "IN_PROGRESS",
    "service": "Network",
    "created_by": "user2",
    "created_at": "2026-10-28T11:00:00"
  }
]
```

The CSV input uses the same field names as its header row.

## Ticket Processing Workflow

The application follows this processing sequence:

1. The CLI parses the input file argument.
2. `TicketService` coordinates the processing workflow.
3. `FileLoader` reads the JSON or CSV records.
4. `TicketInput` validates the incoming ticket data using Pydantic.
5. The validated data is converted into a `Ticket` domain object.
6. `TicketProcessor` determines the category, critical status, and description length.
7. `TicketOutput` represents the processed result.
8. The CLI logs the outcome and displays the processed tickets.

## Categorization Rules

Ticket categories are assigned using keywords found in the description.

| Category | Example keywords |
|---|---|
| DATABASE | database, db, sql |
| NETWORK | network, connection, timeout |
| SERVER | server, cpu, memory |
| ACCESS | login, password, authentication |
| GENERAL | Used when no configured keyword matches |

The processor checks the categories in the order implemented in `ticket_processor.py`. If a description matches more than one category, the first matching rule takes precedence.

A ticket is marked critical when its priority is `P1`.

## Logging and Error Handling

The application uses a configured logger to record processing progress and errors.

Expected error scenarios include:

- Input file does not exist.
- Input file has an unsupported extension.
- JSON input is malformed or has an unexpected structure.
- Ticket data fails Pydantic validation.

The CLI returns:

| Exit code | Meaning |
|---|---|
| `0` | Successful execution |
| `1` | Processing failure |

Validation errors are logged separately from custom ticket-processing errors. Unexpected exceptions are logged with traceback information to support debugging.

## Running Tests

The project uses pytest for automated testing.

### Run the complete test suite

```bash
python -m pytest -v
```

### Run CLI tests only

```bash
python -m pytest -v tests/test_process_tickets.py
```

### Run file-loader tests

```bash
python -m pytest -v tests/test_file_loader.py
```

### Run validation tests

```bash
python -m pytest -v tests/test_ticket_models.py
```

The current test suite contains 45 passing tests, including tests for file loading, validation, processing, logging, configuration, exceptions, and CLI behavior.

Run the tests again after making code changes to verify that existing behavior remains correct.

## Configuration

Application settings are defined in `config/settings.py`.

Current settings include:

- Project root directory
- Data directory
- Application name and version
- Logging level
- Default input file

The settings module supports environment-variable configuration and loading values from a `.env` file when present.

## Current Scope and Future Improvements

The current implementation is a local, file-based ticket-processing application. It uses deterministic keyword-based categorization rather than machine learning or an LLM.

Possible future improvements include:

- Add a FastAPI service.
- Store tickets in PostgreSQL.
- Add structured JSON output.
- Add per-record error reporting so one invalid ticket does not stop the entire batch.
- Introduce configurable categorization rules.
- Add Docker support and CI workflows.
- Add metrics and production monitoring.

## License

No license has been specified yet. Add an appropriate license before distributing the project for reuse.
```
