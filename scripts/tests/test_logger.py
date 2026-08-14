from pathlib import Path

from scripts.core.logger import OmegaLogger


def test_logger_creates_instance():
    logger = OmegaLogger(
        name="omega-test-logger",
    )

    assert logger.name == "omega-test-logger"
    assert logger.logger is not None


def test_logger_has_handlers():
    logger = OmegaLogger(
        name="omega-handler-test",
    )

    assert len(logger.logger.handlers) >= 1


def test_logger_methods_do_not_raise(tmp_path):
    logger = OmegaLogger(
        name="omega-method-test",
    )

    target = tmp_path / "example.py"

    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.success("success")
    logger.created(target)
    logger.skipped(target)
    logger.failed(target, RuntimeError("test"))

    assert True
