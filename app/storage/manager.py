from pathlib import Path

from app.config import Config


class StorageManager:

    def __init__(self):

        self.base_path = (
            Path(Config.DATA_DIR)
            / "storage"
        )

        self.base_path.mkdir(
            parents=True,
            exist_ok=True
        )

    def status(self):

        total_files = 0
        total_bytes = 0

        for file in self.base_path.rglob("*"):

            if file.is_file():

                total_files += 1

                try:
                    total_bytes += (
                        file.stat().st_size
                    )
                except OSError:
                    pass

        return {
            "path": str(
                self.base_path
            ),
            "files": total_files,
            "bytes": total_bytes
        }

    def reset(self):

        for file in self.base_path.rglob("*"):

            if file.is_file():

                try:
                    file.unlink()
                except OSError:
                    pass

        return self.status()


storage_manager = StorageManager()
