from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

def generate_email(recipient_name, purpose, tone):

    prompt = f"""
Write a {tone.lower()} professional email.

Tone: {tone}

Recipient: {recipient_name}
Purpose: {purpose}

Format:
Subject: <subject>
Body: <body>
"""

    response = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[
            {"role": "system", "content": "You are an expert email writing assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content