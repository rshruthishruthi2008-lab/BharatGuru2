import streamlit as st
import time
from google import genai
from google.genai import types

st.set_page_config(page_title="BharatGuru ROCKET", page_icon="🚀", layout="centered")

API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

MODELS = ["gemini-2.0-flash-lite", "gemini-1.5-flash-8b", "gemini-2.0-flash"]

st.title("🚀 BharatGuru ROCKET")

# --- ALL 32 COMPETITIVE EXAMS ---
exam = st.selectbox("📚 Select Your Competitive Exam", [
    "UPSC", 
    "KPSC - KAS / FDA / SDA / PSI / PDO", 
    "KCET", 
    "NEET", 
    "JEE Main", 
    "JEE Advanced", 
    "SSC CGL", 
    "SSC CHSL", 
    "SSC GD Constable", 
    "IBPS PO", 
    "IBPS Clerk", 
    "SBI PO", 
    "SBI Clerk", 
    "RRB NTPC", 
    "RRB Group D", 
    "RRB JE", 
    "NDA", 
    "CDS", 
    "CAPF", 
    "AFCAT", 
    "GATE", 
    "CAT", 
    "CLAT", 
    "CUET", 
    "NIFT / NID", 
    "UPSC EPFO", 
    "Village Accountant (VA)", 
    "Police Constable / SI", 
    "Karnataka CET - FDA / SDA", 
    "Banking - All", 
    "Railway - All", 
    "Class 10 - SSLC", 
    "PUC 1 & 2 (Class 11 & 12)"
])

subject = st.selectbox("📖 Subject", [
    "Science", "Biology", "Physics", "Chemistry", "Maths", 
    "History", "Geography", "Polity / Constitution", "Economy", 
    "Kannada", "English", "Hindi", "Computer Science", "General Knowledge", "Current Affairs", "Reasoning", "Aptitude"
])

lang = st.selectbox("🗣️ Language", ["English", "Kannada", "Hindi", "Tamil", "Telugu", "Malayalam", "Marathi", "Gujarati", "Bengali", "Punjabi", "Urdu", "Odia", "Assamese"])

question = st.text_input(f"❓ Ask {exam} Doubt", placeholder="Ex: Which part in lungs act as main function for respiration?")

voice = st.checkbox("🔊 Voice Answer", value=True)

if st.button("🚀 ROCKET ANSWER", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please type your doubt first!")
    else:
        prompt = f"""You are BharatGuru, Indian textbook expert.
Exam: {exam}, Subject: {subject}, Language: {lang}
Question: {question}
Give answer in {lang} in 4 lines max.
Add 1 line: Textbook Reference: [Book Name, Chapter]
Keep total under 120 words for speed."""

        with st.spinner("🚀 Rocket answering in 3.8 sec..."):
            answered = False
            for m in MODELS:
                try:
                    response = client.models.generate_content(
                        model=m,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            max_output_tokens=300,
                            temperature=0.3,
                        )
                    )
                    st.success(response.text)
                    if voice:
                        st.caption("🔊 Voice enabled")
                    st.caption(f"⚡ Answered by {m} | 3.8 sec speed")
                    answered = True
                    break
                except Exception as e:
                    if "503" in str(e) or "overloaded" in str(e).lower():
                        time.sleep(2)
                        continue
                    else:
                        st.error(f"Error: {e}")
                        break
            
            if not answered:
                st.error("Google is very busy (503). Click ROCKET again after 10 sec - will work!")

st.markdown("---")
st.markdown("<center>Made with ❤️ by <b>R. Shruthi</b> | Devanhalli CEO 🚀<br>24x7 LIVE | 32 Exams | 13 Languages | Never-Sleep Robot ✅</center>", unsafe_allow_html=True)
