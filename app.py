import streamlit as st
import time
from google import genai
from google.genai import types
from gtts import gTTS
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="BharatGuru ROCKET 12.0", page_icon="🚀", layout="centered")
st.link_button(
    label="📲 Download Android App",
    url="https://google.com",
    type="primary"
)
API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-3-flash-preview"]

st.title("🚀 BharatGuru ROCKET 12.0")
st.caption("ALL Subjects | 100% Correct | Full & Clear")

exam = st.selectbox("📚 Exam", ["PUC 1 & 2", "Class 10 - SSLC", "UPSC", "KPSC - KAS / FDA / SDA / PSI", "KCET", "NEET", "JEE Main", "SSC CGL", "IBPS PO", "RRB NTPC", "NDA", "GATE", "CAT", "CUET"])
subject = st.selectbox("📖 Subject", ["Science", "Physics", "Chemistry", "Biology", "Maths", "History", "Geography", "Polity", "Economy", "Current Affairs", "GK", "Kannada", "English", "Hindi", "Computer Science", "Reasoning"])
lang = st.selectbox("🗣️ Language", ["English", "Kannada", "Hindi", "Tamil", "Telugu", "Malayalam", "Marathi", "Gujarati", "Bengali"])

uploaded_file = st.file_uploader("📸 Upload Photo Doubt", type=["jpg","png","jpeg"])
question = st.text_input(f"❓ Ask {exam} - {subject} Doubt")
voice_on = st.checkbox("🔊 Voice Answer", value=True)

def create_pdf(text, exam_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, f"BharatGuru - {exam_name} - R. Shruthi CEO", ln=True, align='C')
    pdf.ln(5)
    safe = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, safe)
    return bytes(pdf.output())

if st.button("🚀 ROCKET ANSWER", type="primary", use_container_width=True):
    if not question.strip() and not uploaded_file:
        st.warning("Type or upload photo!")
    else:
        if subject == "Current Affairs":
            subject_rule = "Give 100% LATEST 2025-2026 Current Affairs. Include: Date, Place, Why in news, Background, Significance, Karnataka connection if any. Facts with PIB/The Hindu source."
        elif subject in ["Science", "Physics", "Chemistry", "Biology"]:
            subject_rule = "Give Definition, Law/Principle, Formula with SI unit, Working/Process, Real-life Example, Uses. Formulas must be 100% correct. NCERT level."
        elif subject in ["History", "Geography", "Polity", "Economy"]:
            subject_rule = "Give Introduction, Timeline/Dates, Key Points in bullets, Important Personalities/Places, Significance. Dates must be 100% correct. NCERT + Karnataka textbook."
        elif subject == "Maths":
            subject_rule = "Give Definition, Standard Formulas (correct), Step-by-step Derivation, Solved Example for THIS exact question, Common Mistakes. All formulas must be mathematically correct."
        else:
            subject_rule = "Give Definition, Detailed Explanation in points, Examples, Importance, Summary. Textbook level, clear and full."

        final_prompt = f"""
You are BharatGuru - Senior {exam} expert teacher for {subject} with 20 years experience. Teach in {lang}.

Student Doubt: {question}
Exam: {exam}
Subject: {subject}

INSTRUCTIONS:
1. SUBJECT RULE: {subject_rule}
2. STRUCTURE:
   Topic:
   Definition / Introduction:
   Detailed Explanation: (300-400 words, points)
   Key Points / Formulas / Dates: (In box, 100% correct)
   Example / Application:
   Textbook Reference: (Exact Book, Chapter)
   Quick Revision: (3 points)
3. LANGUAGE: Answer fully in {lang}, clear PUC/UPSC level.
4. CORRECTNESS: Facts, Dates, Formulas must be 100% correct. No hallucination.
5. LENGTH: 400-500 words, full, never cut mid-sentence.
"""

        contents = [final_prompt]
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Doubt Photo", use_column_width=True)
            contents.append(img)

        with st.spinner(f"🚀 Checking {subject} expert..."):
            for m in MODELS:
                try:
                    resp = client.models.generate_content(
                        model=m,
                        contents=contents,
                        config=types.GenerateContentConfig(max_output_tokens=4096, temperature=0.2)
                    )
                    answer = resp.text
                    st.markdown(answer)
                    st.caption(f"✅ {subject} Expert: {m} | Full Clear Correct | {exam}")

                    if voice_on:
                        try:
                            lc = "kn" if lang == "Kannada" else "hi" if lang == "Hindi" else "en"
                            tts = gTTS(text=answer[:1000], lang=lc, slow=False)
                            tts.save("answer.mp3")
                            st.audio("answer.mp3")
                        except:
                            pass

                    pdf_bytes = create_pdf(answer, f"{exam}_{subject}")
                    st.download_button("📄 Download Full PDF", data=pdf_bytes, file_name=f"{subject}_Full.pdf", mime="application/pdf", use_container_width=True)
                    break
                except Exception as e:
                    if "404" in str(e) or "503" in str(e):
                        time.sleep(1)
                        continue
                    st.error(str(e)[:300])
                    break

st.markdown("---")
st.markdown("<center>Made by <b>R. Shruthi</b> | Devanhalli CEO</center>", unsafe_allow_html=True)
st.markdown("<center>ALL Subjects - Clear | Full | Correct</center>", unsafe_allow_html=True)
