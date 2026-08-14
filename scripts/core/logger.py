from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

from .configuration import config


class OmegaLogger:
    """Central logging service for OCGF."""

    def __init__(
        self,
        name: str = "omega-generator",
    ) -> None:
        self.name = name

        self.logger = logging.getLogger(name)

        self.logger.setLevel(logging.DEBUG)

        self.logger.propagate = False

        self._configure()

    def _configure(self) -> None:
        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler(
            sys.stdout
        )

        console_handler.setLevel(
            logging.INFO
        )

        console_handler.setFormatter(
            formatter
        )

        self.logger.addHandler(
            console_handler
        )

        log_file = (
            config.log_directory
            / "omega-generator.log"
        )

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8",
        )

        file_handler.setLevel(
            logging.DEBUG
        )

        file_handler.setFormatter(
            formatter
        )

        self.logger.addHandler(
            file_handler
        )

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def exception(self, message: str) -> None:
        self.logger.exception(message)

    def success(self, message: str) -> None:
        self.logger.info(
            f"[SUCCESS] {message}"
        )

    def created(self, path: Path) -> None:
        self.logger.info(
            f"[CREATE] {path}"
        )

    def skipped(self, path: Path) -> None:
        self.logger.info(
            f"[SKIP] {path}"
        )

    def failed(self, path: Path, error: Exception) -> None:
        self.logger.error(
            f"[FAILED] {path}: {error}"
        )

    def banner(self) -> None:
        self.logger.info("=" * 70)
        self.logger.info(
            f"{config.project_name} "
            f"Code Generation Framework"
        )
        self.logger.info(
            f"OCGF version: {config.version}"
        )
        self.logger.info(
            f"Started: {datetime.now().isoformat()}"
        )
        self.logger.info("=" * 70)


logger = OmegaLogger()