import logging
import os
from datetime import datetime

class DailyFileHandler(logging.Handler):
    def __init__(self, folder_path, level=logging.NOTSET):
        super().__init__(level)
        self.folder_path = folder_path
        os.makedirs(self.folder_path, exist_ok=True)
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self._open_file()

    def _open_file(self):
        log_file = os.path.join(self.folder_path, f"{self.current_date}.log")
        self.stream = open(log_file, "a", encoding="utf-8")

    def emit(self, record):
        try:
            now = datetime.now().strftime("%Y-%m-%d")
            if now != self.current_date:
                self.stream.close()
                self.current_date = now
                self._open_file()
            msg = self.format(record)
            self.stream.write(msg + "\n")
            self.flush()
        except Exception:
            self.handleError(record)

    def flush(self):
        if self.stream and not self.stream.closed:
            self.stream.flush()

    def close(self):
        if self.stream:
            self.stream.close()
        super().close()
