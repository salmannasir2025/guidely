import logging
from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from .config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_starttls,
    MAIL_SSL_TLS=settings.mail_ssl_tls,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(
    recipients: List[str], subject: str, body: str
) -> None:
    """
    Sends an email to a list of recipients.

    Args:
        recipients: A list of email addresses.
        subject: The email subject.
        body: The email body, which can be HTML.
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        logging.info(f"Email sent to {recipients}")
    except Exception as e:
        logging.error(
            f"Failed to send email to {recipients}",
            extra={"error": str(e)},
        )