from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateNotFound,
)

from .configuration import config
from .exceptions import TemplateError


class TemplateEngine:
    """Jinja2 template rendering service."""

    def __init__(
        self,
        template_directory: Path | None = None,
    ) -> None:

        self.template_directory = (
            template_directory
            or config.template_directory
        )

        self.environment = Environment(
            loader=FileSystemLoader(
                str(self.template_directory)
            ),
            undefined=StrictUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def render(
        self,
        template_name: str,
        context: dict[str, Any] | None = None,
    ) -> str:

        context = context or {}

        try:

            template = (
                self.environment.get_template(
                    template_name
                )
            )

            return template.render(**context)

        except TemplateNotFound as exc:

            raise TemplateError(
                f"Template not found: "
                f"{template_name}"
            ) from exc

        except Exception as exc:

            raise TemplateError(
                f"Failed rendering "
                f"{template_name}: {exc}"
            ) from exc

    def exists(
        self,
        template_name: str,
    ) -> bool:

        try:
            self.environment.get_template(
                template_name
            )
            return True

        except TemplateNotFound:
            return False


template_engine = TemplateEngine()