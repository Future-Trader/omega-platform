from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


class ConfigurationError(Exception):
    """Raised when OCGF configuration is invalid."""


@dataclass(slots=True)
class GeneratorConfig:
    """Central configuration for the OMEGA Code Generation Framework."""

    project_name: str = "OMEGA Platform"
    project_code: str = "OMEGA"

    version: str = "1.0.0"

    author: str = "Future-Trader"

    root_directory: Path = field(
        default_factory=lambda: Path(__file__).resolve().parents[2]
    )

    overwrite: bool = False
    dry_run: bool = False
    verbose: bool = True

    template_directory: Path | None = None
    generator_directory: Path | None = None
    log_directory: Path | None = None
    manifest_directory: Path | None = None

    environment: str = "development"

    def __post_init__(self) -> None:
        self.root_directory = Path(self.root_directory).resolve()

        if self.template_directory is None:
            self.template_directory = (
                self.root_directory / "scripts" / "templates"
            )

        if self.generator_directory is None:
            self.generator_directory = (
                self.root_directory / "scripts" / "generators"
            )

        if self.log_directory is None:
            self.log_directory = self.root_directory / ".logs"

        if self.manifest_directory is None:
            self.manifest_directory = (
                self.root_directory / ".omega"
            )

        self.load_environment()
        self.validate()

    @staticmethod
    def _env_bool(name: str, default: bool) -> bool:
        value = os.getenv(name)

        if value is None:
            return default

        return value.strip().lower() in {
            "1",
            "true",
            "yes",
            "y",
            "on",
        }

    def load_environment(self) -> None:
        """Load configuration overrides from environment variables."""

        self.environment = os.getenv(
            "OMEGA_ENVIRONMENT",
            self.environment,
        )

        self.overwrite = self._env_bool(
            "OMEGA_OVERWRITE",
            self.overwrite,
        )

        self.dry_run = self._env_bool(
            "OMEGA_DRY_RUN",
            self.dry_run,
        )

        self.verbose = self._env_bool(
            "OMEGA_VERBOSE",
            self.verbose,
        )

    def validate(self) -> None:
        """Validate configuration and required directories."""

        if not self.project_name.strip():
            raise ConfigurationError(
                "project_name cannot be empty"
            )

        if not self.project_code.strip():
            raise ConfigurationError(
                "project_code cannot be empty"
            )

        if not self.version.strip():
            raise ConfigurationError(
                "version cannot be empty"
            )

        if not self.root_directory.exists():
            raise ConfigurationError(
                f"Root directory does not exist: "
                f"{self.root_directory}"
            )

        self.template_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.generator_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.manifest_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def summary(self) -> dict[str, object]:
        """Return a serializable configuration summary."""

        return {
            "project_name": self.project_name,
            "project_code": self.project_code,
            "version": self.version,
            "author": self.author,
            "environment": self.environment,
            "root_directory": str(self.root_directory),
            "template_directory": str(
                self.template_directory
            ),
            "generator_directory": str(
                self.generator_directory
            ),
            "log_directory": str(
                self.log_directory
            ),
            "manifest_directory": str(
                self.manifest_directory
            ),
            "overwrite": self.overwrite,
            "dry_run": self.dry_run,
            "verbose": self.verbose,
        }


config = GeneratorConfig()