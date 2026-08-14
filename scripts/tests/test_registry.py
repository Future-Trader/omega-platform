import pytest

from scripts.core.exceptions import RegistryError
from scripts.core.registry import GeneratorRegistry


def sample_generator(**kwargs):
    return {"created": ["example.py"]}


def test_register_generator():
    registry = GeneratorRegistry()

    registry.register(
        "auth",
        "Authentication generator",
        sample_generator,
    )

    assert registry.exists("auth")
    assert registry.names() == ["auth"]


def test_register_normalizes_name():
    registry = GeneratorRegistry()

    registry.register(
        "  AUTH  ",
        "Authentication generator",
        sample_generator,
    )

    assert registry.exists("auth")


def test_duplicate_registration_raises():
    registry = GeneratorRegistry()

    registry.register(
        "auth",
        "Authentication generator",
        sample_generator,
    )

    with pytest.raises(RegistryError):
        registry.register(
            "auth",
            "Duplicate generator",
            sample_generator,
        )


def test_unknown_generator_raises():
    registry = GeneratorRegistry()

    with pytest.raises(RegistryError):
        registry.get("missing")


def test_unregister_generator():
    registry = GeneratorRegistry()

    registry.register(
        "auth",
        "Authentication generator",
        sample_generator,
    )

    registry.unregister("auth")

    assert not registry.exists("auth")
    assert registry.names() == []
