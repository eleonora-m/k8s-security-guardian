import json

class AuditLogParser:
    def __init__(self, log_path="/var/log/kubernetes/audit.log"):
        self.log_path = log_path

    def detect_suspicious_activity(self):
        """
        Parses Kubernetes audit logs to find unauthorized access attempts.
        (Mock implementation for MVP presentation)
        """
        suspicious_events = []

        # Example pattern for bare-metal environment log inspection
        mock_logs = [
            {"user": "system:anonymous", "verb": "delete", "resource": "secrets", "code": 403},
            {"user": "dev-user", "verb": "create", "resource": "pods/exec", "code": 201}
        ]

        for event in mock_logs:
            if event.get("code") == 403 or event.get("resource") == "pods/exec":
                suspicious_events.append({
                    "alert": "Suspicious API activity detected",
                    "user": event.get("user"),
                    "action": event.get("verb"),
                    "target": event.get("resource")
                })

        return suspicious_events
