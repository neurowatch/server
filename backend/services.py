from django.core.mail import send_mail
from firebase_admin import messaging

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def send_email(recipient, clip_id):
    try:
        # Sends an email notifying of the detected movment. Since this is a test and no domain name is present, localhost is used. If this were used in 
        # a production environment the actual domain name should be used
        send_mail(
            subject="Alert - Movement Detected",
            message=
                f'''
                    Neurowatch has detected movement in a room.
                    Check it here: http://192.168.1.20:8000/clip/{clip_id}/
                ''',
            from_email="alert@neurowatch.com",
            recipient_list=[recipient],
            fail_silently=False,
        )
    except:
        logger.debug("Email sending failed")

def send_push(token):
    message = messaging.Message(
        notification = messaging.Notification(
            title="Neurowatch Alert",
            body="Movement has been detected!",
        ),
        token=token,
    )
    messaging.send(message)