import streamlit as st
from gtts import gTTS
from google import genai

st.set_page_config(page_title="BharatGuru ROCKET", page_icon="🚀", layout="wide")
st.title("🚀 BharatGuru ROCKET - Fastest + Textbook")

# LOAD AQ KEY from Secrets
try:
    API_KEY = st.secrets["API_KEY"]
    API_KEY = API_KEY.strip().strip('"').strip("'")
except:
    API_KEY = ""

if not API_KEY:
    st.error("❌ Add API_KEY in Streamlit Secrets!")
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
        prompt = f"You are BharatGuru for {exam} {subject}. Answer in {lang_name} language in 5 short points. Add TEXTBOOK REF chapter at end. Question: {question}"
        with st.spinner("⚡ Rocket answering..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                ans = response.text
                st.success(ans)
                st.info(f"📚 Reference: NCERT/Karnataka {subject} - {exam}")
                if voice_on:
                    try:
                        tts = gTTS(text=ans[:3000], lang=lang_map[lang_name])
                        tts.save("ans.mp3")
                        st.audio("ans.mp3")
                    except:
                        st.write("Voice not available for this language")
            except Exception as e:
                st.error(f"Error: {e}")
