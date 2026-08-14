from pathlib import Path

from scripts.core.file_writer import FileWriter


def test_file_writer_creates_file(tmp_path):
    writer = FileWriter()

    target = tmp_path / "example.txt"

    result = writer.write(
        target,
        "hello",
        overwrite=True,
    )

    assert result.created is True
    assert result.overwritten is False
    assert result.skipped is False
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "hello"


def test_file_writer_skips_existing_file(tmp_path):
    writer = FileWriter()

    target = tmp_path / "example.txt"
    target.write_text("original", encoding="utf-8")

    result = writer.write(
        target,
        "changed",
        overwrite=False,
    )

    assert result.created is False
    assert result.overwritten is False
    assert result.skipped is True
    assert target.read_text(encoding="utf-8") == "original"


def test_file_writer_overwrites_existing_file(tmp_path):
    writer = FileWriter()

    target = tmp_path / "example.txt"
    target.write_text("original", encoding="utf-8")

    result = writer.write(
        target,
        "changed",
        overwrite=True,
    )

    assert result.created is False
    assert result.overwritten is True
    assert result.skipped is False
    assert target.read_text(encoding="utf-8") == "changed"


def test_file_writer_creates_parent_directories(tmp_path):
    writer = FileWriter()

    target = (
        tmp_path
        / "nested"
        / "folder"
        / "example.txt"
    )

    result = writer.write(
        target,
        "nested content",
        overwrite=True,
    )

    assert result.created is True
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "nested content"


def test_file_writer_dry_run_does_not_write(tmp_path):
    from scripts.core.configuration import config

    writer = FileWriter()

    original = config.dry_run

    try:
        config.dry_run = True

        target = tmp_path / "dry-run.txt"

        result = writer.write(
            target,
            "should not exist",
            overwrite=True,
        )

        assert result.skipped is False
        assert not target.exists()

    finally:
        config.dry_run = original
