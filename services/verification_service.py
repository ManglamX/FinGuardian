import uuid

class VerificationService:
    def __init__(self):
        self.pending_verifications = {}

    def trigger_verification(self, user_id: str, transaction_id: str, method: str = "SMS"):
        """
        Triggers a verification request (Mock).
        """
        req_id = str(uuid.uuid4())
        self.pending_verifications[req_id] = {
            "user_id": user_id,
            "transaction_id": transaction_id,
            "status": "PENDING",
            "method": method
        }
        print(f"[Verification] Triggered {method} for User {user_id}, ReqID: {req_id}")
        return req_id

    def verify_response(self, req_id: str, response: str) -> bool:
        """
        Validates user response.
        """
        if req_id in self.pending_verifications:
            if response == "YES":
                self.pending_verifications[req_id]["status"] = "VERIFIED"
                return True
            else:
                self.pending_verifications[req_id]["status"] = "DENIED"
                return False
        return False

verification_service = VerificationService()
