from __future__ import annotations

from pathlib import Path

from .exceptions import GeneratorError


class Validator:
    """Validation utilities for the OMEGA Code Generation Framework."""

    def require_directory(
        self,
        path: str | Path,
    ) -> Path:
        target = Path(path)

        if not target.exists():
            raise GeneratorError(
                f"Directory does not exist: {target}"
            )

        if not target.is_dir():
            raise GeneratorError(
                f"Path is not a directory: {target}"
            )

        return target

    def require_file(
        self,
        path: str | Path,
    ) -> Path:
        target = Path(path)

        if not target.exists():
            raise GeneratorError(
                f"File does not exist: {target}"
            )

        if not target.is_file():
            raise GeneratorError(
                f"Path is not a file: {target}"
            )

        return target

    def require_non_empty(
        self,
        value: str,
        field_name: str = "value",
    ) -> str:
        if not value or not value.strip():
            raise GeneratorError(
                f"{field_name} cannot be empty."
            )

        return value

    def require_template(
        self,
        template_directory: str | Path,
        template_name: str,
    ) -> Path:
        directory = self.require_directory(
            template_directory
        )

        template = directory / template_name

        if not template.exists():
            raise GeneratorError(
                f"Template does not exist: {template}"
            )

        if not template.is_file():
            raise GeneratorError(
                f"Template is not a file: {template}"
            )

        return template


validator = Validator()
