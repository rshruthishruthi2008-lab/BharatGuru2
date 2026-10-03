import streamlit as st
import time
from google import genai
from google.genai import types
from gtts import gTTS
import os

st.set_page_config(page_title="BharatGuru ROCKET", page_icon="🚀", layout="centered")

API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

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
voice_on = st.checkbox("🔊 Enable Voice Answer", value=True)

if st.button("🚀 ROCKET ANSWER", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Type doubt!")
    else:
        # --- SMART DESCRIPTIVE LOGIC ---
        if exam in ["Class 10 - SSLC"]:
            length_rule = "Give short 4-5 lines answer, easy language, 100 words"
        elif exam in ["PUC 1 & 2", "KCET", "NEET", "JEE Main", "JEE Advanced"]:
            length_rule = "Give DESCRIPTIVE answer for higher education: Definition, Structure, Function, Importance in points, Example. 250-300 words, PUC textbook level"
        else: # UPSC, KPSC etc
            length_rule = "Give DETAILED UPSC/KPSC level answer: Introduction, Body with points, Conclusion, Textbook Reference. 300-350 words, analytical"

        prompt = f"""You are BharatGuru Indian expert.
Exam: {exam}, Subject: {subject}, Language: {lang}, Question: {question}
Instruction: {length_rule}
Language must be {lang}. At end add: Textbook Reference: [Book, Chapter]
"""

        with st.spinner("🚀 Thinking..."):
            for m in MODELS:
                try:
                    resp = client.models.generate_content(
                        model=m, 
                        contents=prompt, 
                        config=types.GenerateContentConfig(max_output_tokens=800, temperature=0.4)
                    )
                    answer = resp.text
                    st.success(answer)
                    st.caption(f"⚡ {m} | Descriptive Mode for {exam}")

                    # --- AUDIO FIX ---
                    if voice_on:
                        try:
                            lang_code = "kn" if lang=="Kannada" else "hi" if lang=="Hindi" else "en"
                            tts = gTTS(text=answer[:400], lang=lang_code, slow=False)
                            tts.save("answer.mp3")
                            st.audio("answer.mp3", format="audio/mp3")
                            st.caption("🔊 Voice Answer Playing")
                        except Exception as e:
                            st.caption(f"Audio error: {e}")

                    break
                except Exception as e:
                    if "404" in str(e) or "503" in str(e):
                        time.sleep(1)
                        continue
                    st.error(str(e)[:300])
                    break

st.markdown("---")
st.markdown("<center>Made  by <b>R. Shruthi</b> |  CEO 🚀</center>", unsafe_allow_html=True)
