from django.core.mail import send_mail

def send_email_notification():
    send_mail(
        subject="Lo ladrone",
        message="Tan aca",
        from_email="leojg2091@gmail.com",
        recipient_list=["leojg2091@hotmail.com"],
        fail_silently=False,
    )