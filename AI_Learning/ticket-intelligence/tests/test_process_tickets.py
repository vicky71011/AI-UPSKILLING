
import csv
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "process_tickets.py"


def run_cli(*args):
    """Run the CLI script and capture its output."""
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{PROJECT_ROOT}:{PROJECT_ROOT / 'app'}"

    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )


def test_process_valid_csv():
    """Valid CSV should process successfully."""
    result = run_cli("--input", "data/tickets.csv")
    output = result.stdout + result.stderr

    assert result.returncode == 0
    assert "Successfully processed 2 tickets" in output
    assert "INC001" in result.stdout
    assert "INC002" in result.stdout
    assert "DATABASE" in result.stdout
    assert "NETWORK" in result.stdout


def test_missing_input_file():
    """Missing input file should return exit code 1."""
    result = run_cli("--input", "data/does_not_exist.csv")
    output = result.stdout + result.stderr

    assert result.returncode == 1
    assert "Ticket processing failed" in output
    assert "does_not_exist.csv" in output


def test_invalid_ticket_data(tmp_path):
    """Invalid ticket priority should trigger validation handling."""
    invalid_csv = tmp_path / "invalid_tickets.csv"

    fieldnames = [
        "ticket_id",
        "description",
        "priority",
        "status",
        "service",
        "created_by",
        "created_at",
    ]

    with invalid_csv.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                "ticket_id": "INC999",
                "description": "Database connection failure",
                "priority": "P5",
                "status": "OPEN",
                "service": "Database",
                "created_by": "test_user",
                "created_at": "2026-10-28T10:00:00",
            }
        )

    result = run_cli("--input", str(invalid_csv))
    output = result.stdout + result.stderr

    assert result.returncode == 1
    assert "Ticket validation failed" in output


def test_default_input_file():
    """Omitting --input should use the configured default."""
    result = run_cli()
    output = result.stdout + result.stderr

    assert result.returncode == 0
    assert "Processing tickets" in output
    assert "Successfully processed" in output


def test_help_option():
    """Help should display CLI usage and exit successfully."""
    result = run_cli("--help")

    assert result.returncode == 0
    assert "--input" in result.stdout
    assert "Process and categorize support tickets" in result.stdout
