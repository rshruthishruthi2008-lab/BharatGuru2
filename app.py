import streamlit as st
from gtts import gTTS
from google import genai
import time

st.set_page_config(page_title="BharatGuru ROCKET", page_icon="🚀", layout="wide")
st.title("🚀 BharatGuru ROCKET - Fastest + Textbook")

API_KEY = st.secrets.get("API_KEY","").strip().strip('"').strip("'")
if not API_KEY:
    st.error("Add API_KEY in Secrets")
    st.stop()

client = genai.Client(api_key=API_KEY)

lang_map = {"Kannada":"kn","Hindi":"hi","English":"en","Tamil":"ta","Telugu":"te","Malayalam":"ml","Marathi":"mr","Gujarati":"gu","Bengali":"bn","Punjabi":"pa","Odia":"or","Assamese":"as","Urdu":"ur","Sanskrit":"sa","Hinglish":"hi"}
exams = ["Class 5","Class 8","Class 10","Class 12","KPSC","UPSC","NDA","CDS","Railway RRB","Banking","SSC CGL","Police","PSI","FDA/SDA","KCET","NEET","JEE","TET"]
subjects = ["GK","History","Geography","Science","Maths","Physics","Chemistry","Biology","Kannada","English","Current Affairs","Constitution","Computer"]

c1,c2,c3 = st.columns(3)
with c1: exam = st.selectbox("📚 Exam", exams)
with c2: subject = st.selectbox("📖 Subject", subjects)
with c3: lang_name = st.selectbox("🗣️ Language", list(lang_map.keys()))

question = st.text_input(f"❓ Ask {exam} {subject} Doubt")
voice_on = st.checkbox("🔊 Voice", True)

if st.button("🚀 ROCKET ANSWER", type="primary"):
    if not question:
        st.warning("Type question!")
    else:
        prompt = f"You are BharatGuru for {exam} {subject}. Answer in {lang_name} in 5 points. Add textbook ref. Question: {question}"
        models_to_try = ["gemini-flash-latest", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash"]
        
        ans = None
        with st.spinner("⚡ Trying best model..."):
            for model_name in models_to_try:
                try:
                    resp = client.models.generate_content(model=model_name, contents=prompt)
                    ans = resp.text
                    st.toast(f"Used {model_name}")
                    break
                except Exception as e:
                    if "503" in str(e) or "UNAVAILABLE" in str(e):
                        time.sleep(1)
                        continue
                    else:
                        # try next model
                        continue
        
        if ans:
            st.success(ans)
            st.info(f"📚 Ref: Karnataka/NCERT {subject} {exam}")
            if voice_on:
                try:
                    tts = gTTS(text=ans[:2500], lang=lang_map[lang_name])
                    tts.save("ans.mp3")
                    st.audio("ans.mp3")
                except:
                    pass
        else:
            st.error("Google is very busy (503). Please click ROCKET ANSWER again after 10 sec - will work!")

# YOUR NAME FOOTER - YOU DID IT!
st.markdown("---")
st.markdown("### 👩‍💻 Made with ❤️ by R. Shruthi | CEO BharatGuru ROCKET 🚀")
st.markdown("📚 India's First Textbook AI | 13 Languages")
