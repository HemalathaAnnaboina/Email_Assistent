import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# -----------------------------
# NVIDIA Client
# -----------------------------
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# -----------------------------
# Gmail Credentials
# -----------------------------
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def generate_email(recipient_name, purpose):

    prompt = f"""
Write a professional email.

Recipient: {recipient_name}

Purpose:
{purpose}

Return the email in the following format:

Subject: <subject>

Body:
<body>

Keep it professional and concise.
"""

    response = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[
            {
                "role": "system",
                "content": "You are an expert email writing assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content


def send_email(receiver_email, email_text):

    lines = email_text.split("\n")

    subject = "AI Generated Email"

    body = email_text

    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line.replace("Subject:", "").strip()
            break

    msg = EmailMessage()

    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:

        smtp.starttls()

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        smtp.send_message(msg)


def main():

    print("=" * 60)
    print("📧 AI EMAIL AGENT")
    print("=" * 60)

    recipient_name = input("Recipient Name : ")
    receiver_email = input("Recipient Email: ")

    purpose = input("\nDescribe the email:\n> ")

    print("\nGenerating Email...\n")

    email = generate_email(
        recipient_name,
        purpose
    )

    print("=" * 60)
    print(email)
    print("=" * 60)

    choice = input("\nSend this email? (y/n): ")

    if choice.lower() == "y":

        try:

            send_email(
                receiver_email,
                email
            )

            print("\n✅ Email Sent Successfully!")

        except Exception as e:

            print("\n❌ Failed to send email")
            print(e)

    else:

        print("\nEmail Cancelled.")


if __name__ == "__main__":
    main()