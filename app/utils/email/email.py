import smtplib
from email.message import EmailMessage

from .shemas import EmailSchema


class Email:
    @staticmethod
    def send_email(email_schema: EmailSchema, message: EmailMessage) -> None:
        with smtplib.SMTP_SSL(email_schema.smtp_host, email_schema.smtp_port) as server:
            server.login(email_schema.smtp_user, email_schema.smtp_pass)
            server.send_message(
                msg=message,
                from_addr=email_schema.sender,
                to_addrs=email_schema.getter
            )
