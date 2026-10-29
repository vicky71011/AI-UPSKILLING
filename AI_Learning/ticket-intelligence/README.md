# Ticket Intelligence

A modular Python application for validating, processing, and categorizing support tickets from JSON and CSV files.

## Overview

Ticket Intelligence demonstrates practical Python application development through domain modeling, input validation, exception handling, logging, command-line processing, automated testing, static analysis, and continuous integration.

The application loads ticket records, validates their fields, converts them into domain objects, categorizes descriptions using deterministic keyword-based rules, identifies critical tickets, and returns structured results.

## Features

- **JSON and CSV support:** Load ticket records from either file format.
- **Input validation:** Validate and normalize ticket fields using Pydantic.
- **Domain modeling:** Represent tickets using Python dataclasses.
- **Automatic categorization:** Assign categories based on description keywords.
- **Critical ticket detection:** Identify tickets with P1 priority.
- **Structured logging:** Record processing progress and errors.
- **Command-line interface:** Process a specified input file or use the configured default.
- **Error handling:** Handle invalid files, unsupported formats, and ticket validation failures.
- **Automated testing:** Verify behavior with pytest.
- **Code quality:** Check formatting and lint rules using Ruff and type consistency using mypy.
- **Continuous integration:** Run quality checks and tests through GitHub Actions.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application runtime and development |
| Pydantic 2 | Input validation and data normalization |
| Python dataclasses | Domain model |
| python-dotenv | Environment-based configuration |
| pytest | Automated testing |
| pytest-cov | Test coverage reporting |
| Ruff | Formatting and linting |
| mypy | Static type checking |
| setuptools | Python packaging and editable installation |
| GitHub Actions | Continuous integration |

## Project Structure

The following structure describes the main application components. The repository may also contain additional configuration and development files.

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
│   ├── cli.py
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
│   ├── test_models.py
│   ├── test_process_tickets.py
│   ├── test_processor.py
│   ├── test_service.py
│   ├── test_settings.py
│   ├── test_ticket_exceptions.py
│   └── test_ticket_models.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Main components

- **Domain:** Defines the core ticket representation and domain-level validation.
- **Models:** Defines Pydantic input and output models.
- **Processors:** Implements ticket categorization, critical-ticket detection, and description-length calculation.
- **Services:** Coordinates file loading, validation, and processing.
- **Utilities:** Provides file-loading and logging functionality.
- **Configuration:** Defines application settings and default input paths.
- **Scripts:** Contains the command-line processing entry point.
- **Tests:** Covers individual components and end-to-end CLI behavior.

## Prerequisites

- Python 3.12 recommended for the current CI configuration.
- pip.
- Git, if cloning the repository.

Python 3.10 or newer is declared in `pyproject.toml`.

## Installation

Run these commands from the `ticket-intelligence` project directory.

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

### 2. Install the project

Upgrade pip and install the project with its development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Editable installation makes the project importable in the development environment without reinstalling it after every source-code change.

Ensure the `dev` optional dependency group in `pyproject.toml` includes the development tools used by your workflow: pytest, pytest-cov, Ruff, and mypy.

### 3. Verify the environment

```bash
python -m pip check
```

This checks for incompatible or missing installed dependencies.

## Running the Application

The command-line processing entry point is `scripts/process_tickets.py`.

After installing the project in editable mode, run the commands below from the project root.

### Process a CSV file

```bash
python scripts/process_tickets.py --input data/tickets.csv
```

### Process a JSON file

```bash
python scripts/process_tickets.py --input data/tickets.json
```

### Use the configured default input file

```bash
python scripts/process_tickets.py
```

### Display command-line help

```bash
python scripts/process_tickets.py --help
```

The CLI logs the processing status and displays the processed ticket ID, priority, status, service, category, and critical status.

Successful execution returns exit code `0`. Handled processing or validation failures return exit code `1`.

## Ticket Data Format

Each input record contains the following fields:

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

CSV files use the same field names as the header row. The loader reads records from the selected file, and Pydantic validates ticket fields during processing.

## Ticket Processing Workflow

The application follows this processing sequence:

1. The CLI parses the input file argument.
2. `TicketService` coordinates ticket processing.
3. `FileLoader` reads the JSON or CSV records.
4. `TicketInput` validates and normalizes the incoming data.
5. The validated data is converted into a `Ticket` domain object.
6. `TicketProcessor` determines the category, critical status, and description length.
7. `TicketOutput` represents the processed result.
8. The CLI logs the outcome and displays the results.

## Categorization Rules

The processor assigns categories using keywords in the ticket description.

| Category | Example keywords |
|---|---|
| DATABASE | `database`, `db`, `sql` |
| NETWORK | `network`, `connection`, `timeout` |
| SERVER | `server`, `cpu`, `memory` |
| ACCESS | `login`, `password`, `authentication` |
| GENERAL | No configured keyword matches |

Matching is case-insensitive, and keyword matching uses whole-word boundaries. When a description matches multiple categories, the first matching rule takes precedence in the order implemented by `TicketProcessor`.

A ticket is considered critical when its priority is `P1`.

These are deterministic keyword rules, not machine-learning or LLM-based classification.

## Configuration

Application settings are defined in `config/settings.py`.

The settings include:

- `PROJECT_ROOT`: Project root directory.
- `DATA_DIR`: Data directory.
- `APP_NAME`: Application name.
- `APP_VERSION`: Application version.
- `LOG_LEVEL`: Logging level.
- `DEFAULT_INPUT_FILE`: Default input path.

The settings module supports environment variables and loading values from a `.env` file.

A `.env` file can be used for local overrides. Keep secrets and machine-specific configuration out of version control; use `.env.example` to document non-secret configuration options.

## Logging and Error Handling

The application uses a configured Python logger to record processing progress and errors.

Handled error scenarios include:

- Input file does not exist.
- Input path is not a regular file.
- File extension is unsupported.
- JSON content is malformed or has an unexpected structure.
- Ticket records fail Pydantic validation.
- File reading encounters an error.

Custom ticket-processing exceptions distinguish file-processing failures from other application errors. The CLI logs validation errors separately and logs unexpected exceptions with traceback information.

The current processing behavior is fail-fast: an invalid ticket can stop the current file-processing operation.

## Testing and Code Quality

The project uses pytest for automated tests and Ruff and mypy for static quality checks.

### Run all tests

```bash
python -m pytest -v
```

### Run tests with coverage

```bash
python -m pytest --cov=app --cov=config --cov-report=term-missing
```

### Run a specific test module

```bash
python -m pytest -v tests/test_process_tickets.py
```

### Check formatting

```bash
ruff format --check .
```

To format files locally:

```bash
ruff format .
```

### Run lint checks

```bash
ruff check .
```

To apply supported automatic fixes:

```bash
ruff check --fix .
```

Review automatic changes before committing them.

### Run static type checking

```bash
mypy app config
```

### Check installed dependencies

```bash
python -m pip check
```

### Latest validation results

The most recent local validation reported:

- 65 pytest tests passed.
- Ruff formatting check passed.
- Ruff lint check passed.
- mypy reported no issues in 18 source files.
- `pip check` reported no broken requirements.

These results describe the recorded local validation run; run the commands again after making changes.

## Continuous Integration

GitHub Actions runs the project's quality checks and tests automatically on pushes and pull requests targeting `main`.

The workflow is stored at the root of the parent Git repository:

```text
AI-UPSKILLING/
└── .github/
    └── workflows/
        └── ci.yml
```

The Python project lives under `AI_Learning/ticket-intelligence/`. The workflow sets that directory as its working directory before installing dependencies and running the checks.

The CI workflow performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs the project and development dependencies.
4. Checks formatting with Ruff.
5. Runs Ruff lint checks.
6. Runs mypy.
7. Executes pytest with coverage reporting.

The workflow has been verified to complete successfully on GitHub.

This is a continuous integration pipeline. Automated deployment, publishing a package to PyPI, and production hosting are not currently part of this workflow.

## Current Scope and Future Improvements

The current application is a local, file-based ticket-processing tool.

Implemented capabilities include file loading, validation, domain modeling, keyword-based categorization, critical-ticket detection, logging, a CLI, automated tests, and CI quality checks.

Potential future improvements include:

- Add a FastAPI service.
- Store tickets in PostgreSQL.
- Generate structured JSON output.
- Support per-record error reporting and batch processing of valid records when other records fail.
- Make categorization rules configurable.
- Add Docker packaging.
- Add package build and release automation.
- Introduce application metrics and production monitoring.
- Add integration tests against external services if such integrations are introduced.

These are future enhancements, not existing features.

## License

No license has been specified yet. Add an appropriate license before distributing the project for reuse.