from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .configuration import config
from .exceptions import FileGenerationError
from .logger import logger


@dataclass(slots=True)
class WriteResult:
    path: Path
    created: bool
    overwritten: bool
    skipped: bool


class FileWriter:
    """Safe filesystem writer used by generators."""

    def write(
        self,
        path: str | Path,
        content: str,
        *,
        overwrite: bool | None = None,
    ) -> WriteResult:

        target = Path(path)

        if overwrite is None:
            overwrite = config.overwrite

        if target.exists() and not overwrite:

            logger.skipped(target)

            return WriteResult(
                path=target,
                created=False,
                overwritten=False,
                skipped=True,
            )

        if config.dry_run:

            logger.info(
                f"[DRY-RUN] Would write {target}"
            )

            return WriteResult(
                path=target,
                created=not target.exists(),
                overwritten=target.exists(),
                skipped=False,
            )

        try:
            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            existed = target.exists()

            target.write_text(
                content,
                encoding="utf-8",
            )

            if existed:
                logger.info(
                    f"[OVERWRITE] {target}"
                )
            else:
                logger.created(target)

            return WriteResult(
                path=target,
                created=not existed,
                overwritten=existed,
                skipped=False,
            )

        except OSError as exc:

            logger.failed(
                target,
                exc,
            )

            raise FileGenerationError(
                f"Unable to write {target}"
            ) from exc


file_writer = FileWriter()