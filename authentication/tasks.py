from django.core.mail import send_mail


def send_activation_email(email, activation_link):
    send_mail(
        "Activate your Videoflix account",
        f"Please activate your account by clicking this link:\n\n{activation_link}",
        None,
        [email],
        fail_silently=False,
    )