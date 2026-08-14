import pytest

from scripts.core.configuration import GeneratorConfig
from scripts.core.engine import GenerationResult, GeneratorEngine
from scripts.core.exceptions import GeneratorError
from scripts.core.registry import GeneratorRegistry


def make_engine():
    config = GeneratorConfig()
    registry = GeneratorRegistry()
    return config, registry, GeneratorEngine(config, registry)


def test_generation_result_total_files():
    result = GenerationResult(
        generator="auth",
        success=True,
        files_created=["a.py", "b.py"],
        files_modified=["c.py"],
        files_skipped=["d.py"],
    )

    assert result.total_files == 4


def test_engine_runs_generator_returning_dict():
    config, registry, engine = make_engine()

    def generator(**kwargs):
        return {
            "created": ["a.py"],
            "modified": ["b.py"],
            "skipped": ["c.py"],
        }

    registry.register(
        "test",
        "Test generator",
        generator,
    )

    result = engine.run("test")

    assert result.success is True
    assert result.generator == "test"
    assert result.files_created == ["a.py"]
    assert result.files_modified == ["b.py"]
    assert result.files_skipped == ["c.py"]
    assert result.total_files == 3


def test_engine_handles_none_result():
    config, registry, engine = make_engine()

    registry.register(
        "empty",
        "Empty generator",
        lambda **kwargs: None,
    )

    result = engine.run("empty")

    assert result.success is True
    assert result.total_files == 0


def test_engine_returns_generation_result():
    config, registry, engine = make_engine()

    expected = GenerationResult(
        generator="custom",
        success=True,
        files_created=["custom.py"],
    )

    registry.register(
        "custom",
        "Custom generator",
        lambda **kwargs: expected,
    )

    result = engine.run("custom")

    assert result is expected
    assert result.success is True


def test_engine_generator_failure_raises():
    config, registry, engine = make_engine()

    def failing_generator(**kwargs):
        raise RuntimeError("boom")

    registry.register(
        "failing",
        "Failing generator",
        failing_generator,
    )

    with pytest.raises(GeneratorError, match="failing"):
        engine.run("failing")


def test_engine_lists_generators():
    config, registry, engine = make_engine()

    registry.register(
        "auth",
        "Authentication generator",
        lambda **kwargs: None,
    )

    registry.register(
        "api",
        "API generator",
        lambda **kwargs: None,
    )

    generators = engine.list_generators()

    assert len(generators) == 2
    assert generators[0]["name"] == "auth"
    assert generators[0]["description"] == "Authentication generator"
    assert generators[1]["name"] == "api"


def test_engine_run_all():
    config, registry, engine = make_engine()

    registry.register(
        "auth",
        "Authentication generator",
        lambda **kwargs: None,
    )

    registry.register(
        "api",
        "API generator",
        lambda **kwargs: None,
    )

    results = engine.run_all()

    assert len(results) == 2
    assert all(result.success for result in results)
