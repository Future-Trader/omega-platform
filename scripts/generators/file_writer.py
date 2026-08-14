from pathlib import Path


class FileWriter:
    def __init__(self, overwrite=False):
        self.overwrite = overwrite

    def write(self, filepath: Path, content: str):
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if filepath.exists() and not self.overwrite:
            print(f"[SKIP] {filepath}")
            return

        filepath.write_text(content, encoding="utf-8")
        print(f"[CREATE] {filepath}")