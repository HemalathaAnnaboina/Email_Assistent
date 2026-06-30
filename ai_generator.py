from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Use Streamlit Secrets if available, otherwise use .env
api_key = st.secrets.get("NVIDIA_API_KEY", os.getenv("NVIDIA_API_KEY"))

# Check if API key exists
if not api_key:
    raise ValueError(
        "NVIDIA_API_KEY not found. Add it to .env (local) or Streamlit Secrets (deployment)."
    )

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
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
            {
                "role": "system",
                "content": "You are an expert email writing assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content