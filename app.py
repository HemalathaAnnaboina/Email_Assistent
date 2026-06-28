import streamlit as st
from ai_generator import generate_email
from email_sender import send_email

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Email Assistant",
    page_icon="📧",
    layout="centered"
)

# ---------------- PROFESSIONAL BLUE UI ----------------
st.markdown("""
    <style>
    /* ===== BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #0D47A1, #1565C0, #1E88E5);
        background-attachment: fixed;
    }

    /* ===== GLASS CARD ===== */
    .block-container {
        padding: 2rem 3rem;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    }

    /* ===== TITLE ===== */
    h1 {
        text-align: center;
        color: white !important;
        font-size: 42px;
        font-weight: 700;
    }

    /* ===== SUBTITLE ===== */
    .subtitle {
        text-align: center;
        color: #E3F2FD;
        font-size: 16px;
        margin-bottom: 20px;
    }

    /* ===== INPUT FIELDS ===== */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: none;
        padding: 10px;
        background-color: rgba(255,255,255,0.95);
        color: black;
    }

    /* ===== LABELS ===== */
    label {
        color: #E3F2FD !important;
        font-weight: 500;
    }

    /* ===== BUTTONS ===== */
    .stButton>button {
        background: linear-gradient(90deg, #1E88E5, #42A5F5);
        color: white;
        border-radius: 10px;
        padding: 0.6rem;
        font-weight: bold;
        border: none;
        width: 100%;
        transition: 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(90deg, #1565C0, #1E88E5);
        transform: scale(1.03);
    }

    /* ===== SELECT BOX ===== */
    div[data-baseweb="select"] {
        border-radius: 10px;
    }

    hr {
        border: 1px solid rgba(255,255,255,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>📧 AI Email Assistant</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Generate and send professional emails using AI</div>", unsafe_allow_html=True)

st.divider()

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    recipient_name = st.text_input("👤 Recipient Name")

with col2:
    receiver_email = st.text_input("📨 Recipient Email")

purpose = st.text_area("✍️ Email Purpose", height=120)

# ---------------- TONE & STYLE ----------------
col3, col4 = st.columns(2)

with col3:
    tone = st.selectbox(
        "🎭 Select Tone",
        ["Formal", "Friendly", "Urgent", "Apologetic", "Professional"]
    )

with col4:
    style = st.selectbox(
        "🎨 Email Style",
        ["Simple", "Detailed", "Short", "Persuasive"]
    )

st.divider()

# ---------------- SESSION ----------------
if "email" not in st.session_state:
    st.session_state.email = ""

# ---------------- BUTTONS ----------------
col5, col6 = st.columns(2)

generate = col5.button("✨ Generate Email")
send = col6.button("🚀 Send Email")

# ---------------- GENERATE EMAIL ----------------
if generate:
    if recipient_name and purpose:

        with st.spinner("🤖 AI is generating your email..."):
            st.session_state.email = generate_email(
                recipient_name,
                purpose,
                tone
            )

        st.success("Email generated successfully!")

    else:
        st.warning("Please fill all fields")

# ---------------- PREVIEW ----------------
if st.session_state.email:
    st.subheader("📩 Email Preview")
    st.code(st.session_state.email, language="markdown")

# ---------------- SEND EMAIL ----------------
if send:
    if receiver_email and st.session_state.email:

        try:
            text = st.session_state.email

            subject = "AI Generated Email"
            body = text

            for line in text.split("\n"):
                if line.lower().startswith("subject:"):
                    subject = line.replace("Subject:", "").strip()
                if line.lower().startswith("body:"):
                    body = text.split("Body:")[-1].strip()

            send_email(receiver_email, subject, body)

            st.success("🎉 Email sent successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.warning("Generate email first")