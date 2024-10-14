from firebase_admin import credentials, messaging
from flask import request

def send_push_notification():
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=request.json["title"],
                body=request.json["body"]
            ),
            token=request.json["fcm_token"]
        )
        response = messaging.send(message)
        return {"message": "Notification Sent"}, 200
    except Exception as e:
        return {"message": str(e)}, 500
