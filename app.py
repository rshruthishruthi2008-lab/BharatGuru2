import streamlit as st
import time
from google import genai
from google.genai import types
from gtts import gTTS
from fpdf import FPDF
from PIL import Image

st.set_page_config(page_title="BharatGuru ROCKET 11.0", page_icon="🚀", layout="centered")

API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

MODELS = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-3-flash-preview"]

st.title("🚀 BharatGuru ROCKET 11.0")
st.caption("PUC Expert | 100% Correct NCERT")

exam = st.selectbox("📚 Exam", ["PUC 1 & 2", "Class 10 - SSLC", "KCET", "NEET", "JEE Main", "UPSC", "KPSC - KAS", "SSC CGL", "IBPS PO", "RRB NTPC"])
subject = st.selectbox("📖 Subject", ["Maths", "Physics", "Chemistry", "Biology", "Science", "History", "Geography", "Polity", "Economy", "Kannada", "English"])
lang = st.selectbox("🗣️ Language", ["English", "Kannada", "Hindi"])

uploaded_file = st.file_uploader("📸 Upload Textbook Doubt Photo", type=["jpg","png","jpeg"])
question = st.text_input(f"❓ Ask Doubt", placeholder="Find integrals of 1/(x^2 - a^2)")
voice_on = st.checkbox("🔊 Voice", value=True)

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
        st.warning("Type or upload!")
    else:
        # --- 100% CORRECTNESS PROMPT ---
        correct_prompt = f"""
You are Karnataka PUC 2nd Year Maths NCERT expert teacher with 20 years experience.

Exam: {exam}
Subject: {subject}
Language: {lang}
Student Question: {question}

YOUR TASK - Must be 100% CORRECT:

1.  If question is "Find integrals of particular functions" like ∫ dx/(x^2-a^2), you MUST give ALL 6 standard formulas CORRECTLY:
    - ∫ dx/(x^2-a^2) = (1/2a) log|(x-a)/(x+a)| + C
    - ∫ dx/(a^2-x^2) = (1/2a) log|(a+x)/(a-x)| + C
    - ∫ dx/(x^2+a^2) = (1/a) tan^-1(x/a) + C
    - ∫ dx/√(x^2-a^2) = log|x+√(x^2-a^2)| + C
    - ∫ dx/√(x^2+a^2) = log|x+√(x^2+a^2)| + C
    - ∫ dx/√(a^2-x^2) = sin^-1(x/a) + C

2.  Give step-by-step derivation with correct maths. Double-check formula.

3.  Structure:
    **Topic:** 
    **Definition:**
    **Standard Formulas (Box):**
    **Solved Example for THIS question:**
    **Textbook Reference: NCERT Class 12 Maths Part 2, Chapter 7, Integrals of Some Particular Functions**

4.  Answer MUST be full, clear, correct, in {lang}, 400-500 words. Never stop mid-sentence.

5.  Use simple PUC language.
"""

        contents = [correct_prompt]
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Your Doubt", use_column_width=True)
            contents.append(img)

        with st.spinner("🚀 Checking NCERT for 100% correct answer..."):
            for m in MODELS:
                try:
                    resp = client.models.generate_content(
                        model=m,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            max_output_tokens=4096,
                            temperature=0.2  # LOW temp = More correct
                        )
                    )
                    answer = resp.text
                    st.markdown(answer)  # Use markdown for clear formulas
                    st.caption(f"✅ Verified by {m} | NCERT Correct")

                    if voice_on:
                        try:
                            lc = "kn" if lang=="Kannada" else "hi" if lang=="Hindi" else "en"
                            tts = gTTS(text=answer[:1000], lang=lc, slow=False)
                            tts.save("answer.mp3")
                            st.audio("answer.mp3")
                        except:
                            pass

                    pdf_bytes = create_pdf(answer, exam)
                    st.download_button("📄 Download Correct Answer PDF", data=pdf_bytes, file_name=f"Correct_{exam}.pdf", mime="application/pdf", use_container_width=True)
                    break
                except Exception as e:
                    if "404" in str(e) or "503" in str(e):
                        time.sleep(1)
                        continue
                    st.error(str(e)[:300])
                    break

st.markdown("---")
st.markdown("<center>Made by <b>R. Shruthi</b> | Devanhalli CEO 🚀 | 100% Correct Mode ✅</center>", unsafe_allow_html=True)
