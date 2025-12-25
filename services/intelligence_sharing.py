class IntelligenceSharingService:
    def __init__(self):
        # Mock database of shared patterns
        self.shared_patterns = []

    def publish_fraud_pattern(self, pattern: dict):
        """
        Anonymizes and publishes a confirmed fraud pattern.
        """
        anonymized = self._anonymize(pattern)
        self.shared_patterns.append(anonymized)
        # In a real system, this would push to Kafka/PubSub
        print(f"[IntelligenceSharing] Published pattern: {anonymized}")

    def fetch_recent_patterns(self):
        return self.shared_patterns[-10:]

    def _anonymize(self, pattern: dict) -> dict:
        """
        Removes PII from pattern.
        """
        safe_pattern = pattern.copy()
        if "user_id" in safe_pattern:
            del safe_pattern["user_id"]
        if "account_id" in safe_pattern:
            del safe_pattern["account_id"]
        return safe_pattern

intelligence_service = IntelligenceSharingService()
