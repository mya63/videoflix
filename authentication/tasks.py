from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def send_activation_email(email, activation_link):
    html_content = render_to_string(
        "emails/activation_email.html",
        {"activation_link": activation_link},
    )

    email_message = EmailMultiAlternatives(
        subject="Activate your Videoflix account",
        body=f"Activate here: {activation_link}",
        to=[email],
    )

    email_message.attach_alternative(html_content, "text/html")
    email_message.send()