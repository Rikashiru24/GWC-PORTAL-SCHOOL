import os
import smtplib
from pathlib import Path
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
from flask import current_app

# 1. Path Setup (Keep this outside)
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(base_dir))
template_path = Path(project_root) / "app" / "templates" / "emails" / "email_template.html"
image_path = Path(project_root) / "app" / "static" / "img" / "harvin.jpeg"

def send_login_credentials(first_name, email, temp_password):
    # GET CONFIG: Use current_app if available, otherwise fallback to os.getenv
    try:
        sender = current_app.config["EMAIL_SENDER"]
        password_key = current_app.config["EMAIL_PASS"]
    except RuntimeError: # Occurs if running script outside Flask
        from dotenv import load_dotenv
        load_dotenv()
        sender = os.getenv("EMAIL_SENDER")
        password_key = os.getenv("EMAIL_PASS")

    # CREATE MESSAGE INSIDE FUNCTION (Crucial!)
    message = MIMEMultipart()
    display_name = "Golden West Colleges, Inc."

    message["From"] = formataddr((display_name, sender))
    message["To"] = email
    message["Subject"] = "Login Credentials"

    # BUILD BODY
    template = Template(template_path.read_text())
    body = template.substitute(name=first_name, email=email, password=temp_password)
    message.attach(MIMEText(body, "html"))

    # ATTACH IMAGE
    message.attach(MIMEImage(image_path.read_bytes()))

    # SEND
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, password_key)
        smtp.send_message(message)
        print(f"Sent to {email}...")
