from django.core.mail import send_mail

def send_email_notification(recipient, clip_id):
    send_mail(
        subject="Alert - Movement Detected",
        message="Neurowatch has detected movement in a room.",
        from_email="leojg2091@gmail.com",
        recipient_list=[recipient],
        fail_silently=False,
    )