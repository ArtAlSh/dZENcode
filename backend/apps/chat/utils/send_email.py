from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


def send_confirmation_code(key, email):
    send_mail(
        subject="Confirmation code",
        message=f"Confirmation code: {key}",
        html_message="",
        from_email=EMAIL_HOST_USER,
        recipient_list=[email]
    )
