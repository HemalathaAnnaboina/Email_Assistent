import smtplib
from email.message import EmailMessage
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(receiver_email, subject, body):

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)