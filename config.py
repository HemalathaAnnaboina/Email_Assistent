import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = st.secrets.get("EMAIL_ADDRESS") or os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD") or os.getenv("EMAIL_PASSWORD")