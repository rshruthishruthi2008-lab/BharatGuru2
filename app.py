import streamlit as st
import time
from google import genai
from google.genai import types

st.set_page_config(page_title="BharatGuru ROCKET", page_icon="🚀", layout="centered")

API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

# --- ONLY LATEST 2026 MODELS - NO 1.5 - 3.8 sec ---
MODELS = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-3-flash-preview"]

st.title("🚀 BharatGuru ROCKET")

exam = st.selectbox("📚 Select Your Competitive Exam", [
    "UPSC", "KPSC - KAS / FDA / SDA / PSI / PDO", "KCET", "NEET", "JEE Main", "JEE Advanced",
    "SSC CGL", "SSC CHSL", "SSC GD", "IBPS PO", "IBPS Clerk", "SBI PO", "SBI Clerk",
    "RRB NTPC", "RRB Group D", "RRB JE", "NDA", "CDS", "CAPF", "AFCAT",
    "GATE", "CAT", "CLAT", "CUET", "NIFT / NID", "UPSC EPFO", "Village Accountant",
    "Police Constable / SI", "Karnataka CET", "Banking - All", "Railway - All",
    "Class 10 - SSLC", "PUC 1 & 2"
])

subject = st.selectbox("📖 Subject", ["Science", "Biology", "Physics", "Chemistry", "Maths", "History", "Geography", "Polity", "Economy", "Kannada", "English", "Hindi", "Computer Science", "GK", "Current Affairs", "Reasoning", "Aptitude"])
lang = st.selectbox("🗣️ Language", ["English", "Kannada", "Hindi", "Tamil", "Telugu", "Malayalam", "Marathi", "Gujarati", "Bengali", "Punjabi", "Urdu", "Odia", "Assamese"])
question = st.text_input(f"❓ Ask {exam} Doubt")

if st.button("🚀 ROCKET ANSWER", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Type doubt!")
    else:
        prompt = f"Exam:{exam}, Sub:{subject}, Lang:{lang}, Q:{question}. Answer in {lang} in 4 lines + Textbook Ref. Under 120 words."
        with st.spinner("🚀 3.8 sec..."):
            for m in MODELS:
                try:
                    resp = client.models.generate_content(model=m, contents=prompt, config=types.GenerateContentConfig(max_output_tokens=300, temperature=0.3))
                    st.success(resp.text)
                    st.caption(f"⚡ {m}")
                    break
                except Exception as e:
                    if "404" in str(e) or "503" in str(e) or "NOT_FOUND" in str(e):
                        time.sleep(1)
                        continue
                    st.error(str(e)[:200])
                    break

st.markdown("---")
st.markdown("<center>Made with  by <b>R. Shruthi</b> | Devanhalli CEO 🚀</center>", unsafe_allow_html=True)
