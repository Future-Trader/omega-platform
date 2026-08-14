from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .configuration import GeneratorConfig
from .exceptions import GeneratorError
from .registry import GeneratorRegistry


@dataclass(slots=True)
class GenerationResult:
    generator: str
    success: bool
    files_created: list[str] = field(default_factory=list)
    files_modified: list[str] = field(default_factory=list)
    files_skipped: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return (
            len(self.files_created)
            + len(self.files_modified)
            + len(self.files_skipped)
        )


class GeneratorEngine:
    """Execution engine for the OMEGA Code Generation Framework."""

    def __init__(
        self,
        config: GeneratorConfig,
        registry: GeneratorRegistry,
    ) -> None:
        self.config = config
        self.registry = registry

    def list_generators(self) -> list[dict[str, str]]:
        """Return all registered generators."""
        return [
            {
                "name": definition.name,
                "description": definition.description,
            }
            for definition in self.registry.all()
        ]

    def run(
        self,
        name: str,
        **kwargs: Any,
    ) -> GenerationResult:
        """Run one registered generator."""

        definition = self.registry.get(name)

        result = GenerationResult(
            generator=definition.name,
            success=False,
        )

        try:
            output = definition.generator(
                config=self.config,
                **kwargs,
            )

            if output is None:
                result.success = True
                return result

            if isinstance(output, GenerationResult):
                return output

            if isinstance(output, dict):
                result.files_created.extend(
                    str(path)
                    for path in output.get(
                        "created",
                        [],
                    )
                )

                result.files_modified.extend(
                    str(path)
                    for path in output.get(
                        "modified",
                        [],
                    )
                )

                result.files_skipped.extend(
                    str(path)
                    for path in output.get(
                        "skipped",
                        [],
                    )
                )

                result.errors.extend(
                    str(error)
                    for error in output.get(
                        "errors",
                        [],
                    )
                )

                result.success = not result.errors
                return result

            result.success = True
            return result

        except Exception as exc:
            result.errors.append(str(exc))
            raise GeneratorError(
                f"Generator '{name}' failed: {exc}"
            ) from exc

    def run_all(self, **kwargs: Any) -> list[GenerationResult]:
        """Run every registered generator."""

        results: list[GenerationResult] = []

        for definition in self.registry.all():
            results.append(
                self.run(
                    definition.name,
                    **kwargs,
                )
            )

        return results
