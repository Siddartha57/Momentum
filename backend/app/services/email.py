import smtplib
from email.message import EmailMessage
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from app.core.config import settings

env = Environment(loader=FileSystemLoader("app/templates"))

def send_email(to_email: str, subject: str, template_name: str, context: dict):
    if not settings.smtp_host or not settings.smtp_user or not settings.smtp_password:
        print(f"Skipping email to {to_email} (SMTP not configured). Subject: {subject}")
        return

    template = env.get_template(template_name)
    html_content = template.render(**context)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from
    msg["To"] = to_email
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
            print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
