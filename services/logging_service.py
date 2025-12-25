from models.persistence import AuditLog
from datetime import datetime

class LoggingService:
    def __init__(self):
        self.logs = []

    def log_event(self, event_type: str, details: dict):
        log = AuditLog(
            event_type=event_type,
            details=details,
            timestamp=datetime.now()
        )
        self.logs.append(log)
        print(f"[Audit] {event_type}: {details}")

    def get_logs(self, limit: int = 10):
        return self.logs[-limit:]

logging_service = LoggingService()
