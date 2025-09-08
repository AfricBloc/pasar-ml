import logging
import json
import sys

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Attach extras passed in logger calls
        for key, value in record.__dict__.items():
            if key not in logging.LogRecord.__dict__ and key not in log_record:
                log_record[key] = value
        return json.dumps(log_record)

logger = logging.getLogger("pasar")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger.handlers = [handler]
