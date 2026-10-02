import streamlit as st
from gtts import gTTS
from google import genai

API_KEY = "AQ.Ab8RN6IT7DbQ7oqqAF0o4CzLLBLIJ7u12Drznpkm2Elz5SVubg"

st.set_page_config(page_title="BharatGuru Rocket", page_icon="🚀", layout="wide")
st.title("🚀 BharatGuru ROCKET - Fastest + Textbook")

selected_model = "gemini-3.5-flash-lite" # LIT - Fastest for your AQ key
st.sidebar.success(f"⚡ {selected_model} (LIT)")
st.sidebar.checkbox("✅ Anti-Sleep ON", value=True)

lang_map = {"Kannada":"kn","Hindi":"hi","English":"en","Tamil":"ta","Telugu":"te","Malayalam":"ml","Marathi":"mr","Gujarati":"gu","Bengali":"bn","Punjabi":"pa","Odia":"or","Assamese":"as","Urdu":"ur","Sanskrit":"sa","Hinglish":"hi"}
exams = ["Class 5","Class 8","Class 10","Class 12","KPSC","UPSC","NDA","CDS","Railway RRB","Banking","SSC CGL","Police","PSI","FDA/SDA","KCET","NEET","JEE","TET"]
subjects = ["GK","History","Geography","Science","Maths","Physics","Chemistry","Biology","Kannada","English","Current Affairs","Constitution","Computer"]

c1,c2,c3 = st.columns(3)
with c1: exam = st.selectbox("📚 Exam", exams)
with c2: subject = st.selectbox("📖 Subject", subjects)
with c3: lang_name = st.selectbox("🗣️ Language", list(lang_map.keys()))

question = st.text_input(f"❓ Ask {exam} {subject} Doubt", placeholder="Ex: explain corrosion")
voice_on = st.checkbox("🔊 Voice", True)

if st.button("🚀 ROCKET ANSWER", type="primary"):
    if not question:
        st.warning("Type question!")
    else:
        client = genai.Client(api_key=API_KEY)
        prompt = f"You are BharatGuru for {exam} {subject}. Answer in {lang_name} in 5 short points. At end add 📚 TEXTBOOK REF: Karnataka/NCERT exact chapter. Question: {question}"
        with st.spinner("⚡ Answering..."):
            response = client.models.generate_content(model=selected_model, contents=prompt)
            ans = response.text
        st.success(ans)
        st.info(f"📚 Reference: Karnataka/NCERT {subject} - {exam} - Chapter for {question}")
        if voice_on:
            tts = gTTS(text=ans[:3000], lang=lang_map[lang_name])
            tts.save("ans.mp3")
            st.audio("ans.mp3")

st.markdown('<meta http-equiv="refresh" content="1800">', unsafe_allow_html=True)