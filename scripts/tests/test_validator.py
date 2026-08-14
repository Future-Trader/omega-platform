import pytest

from scripts.core.exceptions import GeneratorError
from scripts.core.validator import Validator


def test_require_directory(tmp_path):
    validator = Validator()

    result = validator.require_directory(tmp_path)

    assert result == tmp_path


def test_require_directory_missing(tmp_path):
    validator = Validator()

    missing = tmp_path / "missing"

    with pytest.raises(
        GeneratorError,
        match="Directory does not exist",
    ):
        validator.require_directory(missing)


def test_require_directory_rejects_file(tmp_path):
    validator = Validator()

    target = tmp_path / "example.txt"
    target.write_text("hello", encoding="utf-8")

    with pytest.raises(
        GeneratorError,
        match="not a directory",
    ):
        validator.require_directory(target)


def test_require_file(tmp_path):
    validator = Validator()

    target = tmp_path / "example.txt"
    target.write_text("hello", encoding="utf-8")

    result = validator.require_file(target)

    assert result == target


def test_require_file_missing(tmp_path):
    validator = Validator()

    missing = tmp_path / "missing.txt"

    with pytest.raises(
        GeneratorError,
        match="File does not exist",
    ):
        validator.require_file(missing)


def test_require_file_rejects_directory(tmp_path):
    validator = Validator()

    target = tmp_path / "folder"
    target.mkdir()

    with pytest.raises(
        GeneratorError,
        match="not a file",
    ):
        validator.require_file(target)


def test_require_non_empty():
    validator = Validator()

    assert (
        validator.require_non_empty(
            "OMEGA",
            "project_code",
        )
        == "OMEGA"
    )


def test_require_non_empty_rejects_empty():
    validator = Validator()

    with pytest.raises(
        GeneratorError,
        match="project_code cannot be empty",
    ):
        validator.require_non_empty(
            "",
            "project_code",
        )


def test_require_non_empty_rejects_whitespace():
    validator = Validator()

    with pytest.raises(
        GeneratorError,
        match="project_name cannot be empty",
    ):
        validator.require_non_empty(
            "   ",
            "project_name",
        )


def test_require_template(tmp_path):
    validator = Validator()

    template = tmp_path / "example.j2"
    template.write_text(
        "Hello {{ name }}",
        encoding="utf-8",
    )

    result = validator.require_template(
        tmp_path,
        "example.j2",
    )

    assert result == template


def test_require_template_missing(tmp_path):
    validator = Validator()

    with pytest.raises(
        GeneratorError,
        match="Template does not exist",
    ):
        validator.require_template(
            tmp_path,
            "missing.j2",
        )
