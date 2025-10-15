"""Logging configuration with emoji support"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str = 'form_filler',
    log_to_file: bool = True,
    verbose: bool = False
) -> logging.Logger:
    """
    Setup logger with console and optional file output

    Args:
        name: Logger name
        log_to_file: Whether to also log to file
        verbose: Enable verbose/debug logging

    Returns:
        Configured logger instance

    Examples:
        >>> logger = setup_logger()
        >>> logger.info("Test message")
    """
    logger = logging.getLogger(name)

    # Set level
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    console_formatter = logging.Formatter(
        '%(asctime)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_to_file:
        logs_dir = Path('logs')
        logs_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = logs_dir / f'form_filler_{timestamp}.log'

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        logger.info(f"📁 Log file: {log_file}")

    return logger


class LogColors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'


def log_section(logger: logging.Logger, title: str) -> None:
    """
    Log a section header

    Args:
        logger: Logger instance
        title: Section title
    """
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"  {title}")
    logger.info("=" * 60)


def log_page(logger: logging.Logger, page_name: str, page_num: int) -> None:
    """
    Log current page being processed

    Args:
        logger: Logger instance
        page_name: Name/type of page
        page_num: Page number
    """
    logger.info("")
    logger.info(f"📄 Page {page_num}: {page_name}")


def log_checkbox_change(logger: logging.Logger, label: str, checked: bool) -> None:
    """
    Log checkbox state change

    Args:
        logger: Logger instance
        label: Checkbox label
        checked: New checked state
    """
    icon = "✓" if checked else "☐"
    logger.info(f"  {icon} {label}")


def log_field_fill(logger: logging.Logger, field_name: str, value: any) -> None:
    """
    Log field filling

    Args:
        logger: Logger instance
        field_name: Name/description of field
        value: Value being filled
    """
    logger.info(f"  ✏️  {field_name}: {value}")


def log_table_fill(logger: logging.Logger, topic: str, year: str, value: int) -> None:
    """
    Log table cell filling

    Args:
        logger: Logger instance
        topic: Topic/row name
        year: School year
        value: Count value
    """
    logger.info(f"  📊 {topic} | {year}: {value}")


def log_error(logger: logging.Logger, error_msg: str, exc: Exception = None) -> None:
    """
    Log error with optional exception

    Args:
        logger: Logger instance
        error_msg: Error message
        exc: Optional exception object
    """
    logger.error(f"❌ {error_msg}")
    if exc:
        logger.error(f"   Exception: {type(exc).__name__}: {exc}")


def log_success(logger: logging.Logger, message: str) -> None:
    """
    Log success message

    Args:
        logger: Logger instance
        message: Success message
    """
    logger.info(f"✅ {message}")


def log_warning(logger: logging.Logger, message: str) -> None:
    """
    Log warning message

    Args:
        logger: Logger instance
        message: Warning message
    """
    logger.warning(f"⚠️  {message}")


def log_skip(logger: logging.Logger, page_name: str, reason: str) -> None:
    """
    Log page skip

    Args:
        logger: Logger instance
        page_name: Name of page being skipped
        reason: Reason for skipping
    """
    logger.info(f"⏭️  Skipping {page_name}: {reason}")
