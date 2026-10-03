import streamlit as st
import time
from google import genai
from google.genai import types
from gtts import gTTS
from fpdf import FPDF
from PIL import Image
import io

st.set_page_config(page_title="BharatGuru ROCKET 10.0", page_icon="🚀", layout="centered")

API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

MODELS = ["gemini-2.5-flash-lite", "gemini-2.5-flash", "gemini-3-flash-preview"]

st.title("🚀 BharatGuru ROCKET 10.0")
st.caption("32 Exams | Photo Doubt | PDF + Voice")

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

# --- NEW: PHOTO DOUBT ---
uploaded_file = st.file_uploader("📸 Upload Photo of Doubt (Optional)", type=["jpg","png","jpeg"])

question = st.text_input(f"❓ Ask {exam} Doubt", placeholder="Or just upload photo above")

voice_on = st.checkbox("🔊 Voice Answer", value=True)

def create_pdf(text, exam_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"BharatGuru - {exam_name} - Made by R.Shruthi", ln=True, align='C')
    pdf.ln(10)
    # Clean text for PDF
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    return pdf.output(dest='S').encode('latin-1')

if st.button("🚀 ROCKET ANSWER", type="primary", use_container_width=True):
    if not question.strip() and not uploaded_file:
        st.warning("Type doubt or upload photo!")
    else:
        if exam in ["Class 10 - SSLC"]:
            length_rule = "Short 4-5 lines, 100 words"
        elif exam in ["PUC 1 & 2", "KCET", "NEET", "JEE Main", "JEE Advanced"]:
            length_rule = "DESCRIPTIVE: Definition, Structure, Function, Points, Example. 250-300 words PUC level"
        else:
            length_rule = "DETAILED UPSC level: Intro, Body points, Conclusion. 300-350 words"

        prompt_text = f"Exam:{exam}, Sub:{subject}, Lang:{lang}, Q:{question}. {length_rule}. Answer in {lang}. Add Textbook Ref at end."
        
        contents = [prompt_text]
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Your Doubt Photo", use_column_width=True)
            contents.append(img)

        with st.spinner("🚀 ROCKET Thinking..."):
            for m in MODELS:
                try:
                    resp = client.models.generate_content(
                        model=m,
                        contents=contents,
                        config=types.GenerateContentConfig(max_output_tokens=1000, temperature=0.4)
                    )
                    answer = resp.text
                    st.success(answer)
                    st.caption(f"⚡ {m} | {exam}")

                    # AUDIO
                    if voice_on:
                        try:
                            lc = "kn" if lang=="Kannada" else "hi" if lang=="Hindi" else "en"
                            tts = gTTS(text=answer[:400], lang=lc)
                            tts.save("answer.mp3")
                            st.audio("answer.mp3")
                        except:
                            pass

                    # PDF DOWNLOAD
                    pdf_bytes = create_pdf(answer, exam)
                    st.download_button("📄 Download as PDF", data=pdf_bytes, file_name=f"{exam}_Answer.pdf", mime="application/pdf", use_container_width=True)

                    break
                except Exception as e:
                    if "404" in str(e) or "503" in str(e):
                        time.sleep(1)
                        continue
                    st.error(str(e)[:300])
                    break

st.markdown("---")
st.markdown("<center>Made by <b>R. Shruthi</b> | Devanhalli CEO 🚀<br>Photo Doubt + PDF + Voice ✅</center>", unsafe_allow_html=True)
