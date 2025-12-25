import os
from twilio.rest import Client

def send_sms_alert(message: str, to_number: str):
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_no = os.getenv("TWILIO_FROM_NUMBER")

    if not all([sid, token, from_no]):
        print("[ALERT] Twilio credentials not configured - skipping SMS")
        return  # fail-safe

    try:
        client = Client(sid, token)
        client.messages.create(
            body=message,
            from_=from_no,
            to=to_number
        )
        print(f"[ALERT] SMS sent successfully to {to_number}")
    except Exception as e:
        print(f"[ALERT] Failed to send SMS: {str(e)}")
        # Don't raise - allow the system to continue
