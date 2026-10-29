import logging

from app.utils.logging import get_logger
from config.settings import LOG_LEVEL


def test_logger_name():
    logger = get_logger("test_logger")

    assert logger.name == "test_logger"


def test_logger_level():
    logger = get_logger("test_level_logger")

    expected_level = getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO,
    )

    assert logger.level == expected_level


def test_logger_has_handler():
    logger = get_logger("test_handler_logger")

    assert len(logger.handlers) >= 1


def test_logger_does_not_add_duplicate_handlers():
    logger = get_logger("duplicate_test_logger")
    initial_handler_count = len(logger.handlers)

    get_logger("duplicate_test_logger")

    assert len(logger.handlers) == initial_handler_count


def test_logger_output(capsys):
    logger = get_logger("output_test_logger")
    logger.setLevel(logging.INFO)

    logger.info("Ticket processing started")

    captured = capsys.readouterr()
    output = captured.err + captured.out

    assert "INFO" in output
    assert "output_test_logger" in output
    assert "Ticket processing started" in output
