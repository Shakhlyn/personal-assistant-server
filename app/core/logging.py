import json
import logging
import sys
from datetime import UTC, datetime

from app.core.request_id import get_request_id


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }

        # Pulled from the contextvar, so every log line inside a request is
        # correlated without the call site having to pass anything.
        request_id = getattr(record, "request_id", None) or get_request_id()
        if request_id:
            log["request_id"] = request_id

        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        return json.dumps(log)


def setup_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = [handler]
