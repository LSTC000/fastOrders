from email.message import EmailMessage


class EmailMessages:
    @staticmethod
    def error_log_message(subject: str, error_log: str) -> EmailMessage:
        email = EmailMessage()
        email['Subject'] = subject

        email.set_content(
            '<h1>Error details</h1>'
            f'{error_log}',
            subtype='html'
        )

        return email
