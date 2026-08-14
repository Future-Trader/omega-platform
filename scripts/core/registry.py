from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .exceptions import RegistryError


@dataclass(slots=True)
class GeneratorDefinition:
    name: str
    description: str
    generator: Callable[..., Any]


class GeneratorRegistry:
    """Central registry for OCGF generators."""

    def __init__(self) -> None:
        self._generators: dict[
            str,
            GeneratorDefinition,
        ] = {}

    def register(
        self,
        name: str,
        description: str,
        generator: Callable[..., Any],
    ) -> None:

        normalized = name.strip().lower()

        if not normalized:
            raise RegistryError(
                "Generator name cannot be empty."
            )

        if normalized in self._generators:
            raise RegistryError(
                f"Generator already registered: {name}"
            )

        self._generators[normalized] = (
            GeneratorDefinition(
                name=normalized,
                description=description,
                generator=generator,
            )
        )

    def unregister(self, name: str) -> None:
        normalized = name.strip().lower()

        self._generators.pop(
            normalized,
            None,
        )

    def get(self, name: str) -> GeneratorDefinition:
        normalized = name.strip().lower()

        try:
            return self._generators[normalized]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown generator: {name}"
            ) from exc

    def exists(self, name: str) -> bool:
        return (
            name.strip().lower()
            in self._generators
        )

    def names(self) -> list[str]:
        return sorted(
            self._generators.keys()
        )

    def all(self) -> list[GeneratorDefinition]:
        return list(
            self._generators.values()
        )


registry = GeneratorRegistry()
def register_builtin_generators() -> None:
    """Register generators shipped with OMEGA."""

    from scripts.generators.auth_generator import generate_auth

    if not registry.exists("auth"):
        registry.register(
            name="auth",
            description="Generate Authentication & Security foundation.",
            generator=generate_auth,
        )
