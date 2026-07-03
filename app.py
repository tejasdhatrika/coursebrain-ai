import streamlit as st
import whisper
import os
import json
from src.summarize import generate_summary

st.set_page_config(page_title="CourseBrain AI", page_icon="🧠")

st.title("🧠 CourseBrain AI")
st.write("Upload a lecture recording and generate timestamped transcript.")

UPLOAD_DIR = "data/uploads"
TRANSCRIPT_DIR = "data/transcripts"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

uploaded_file = st.file_uploader(
    "Upload lecture audio/video",
    type=["mp4", "mp3", "wav", "m4a"]
)

@st.cache_resource
def load_model():
    return whisper.load_model("base")

def seconds_to_time(seconds):
    seconds = int(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"

if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("File uploaded successfully")

    if uploaded_file.name.endswith(".mp4"):
        st.video(file_path)
    else:
        st.audio(file_path)

    if st.button("Transcribe Lecture"):
        with st.spinner("Transcribing..."):
            model = load_model()
            result = model.transcribe(file_path)

        transcript_data = []

        for segment in result["segments"]:
            transcript_data.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        transcript_file = os.path.join(
            TRANSCRIPT_DIR,
            uploaded_file.name + ".json"
        )

        with open(transcript_file, "w", encoding="utf-8") as f:
            json.dump(transcript_data, f, indent=4)
        full_transcript = ""

        for segment in transcript_data:
            full_transcript += segment["text"] + " "
        st.success("Transcription completed!")
        summary = generate_summary(full_transcript)

        st.subheader("Lecture Summary")

        st.markdown("### Summary")
        st.write(summary["summary"])

        st.markdown("### Key Concepts")

        for concept in summary["key_concepts"]:
            st.write(f"• {concept}")

        st.markdown("### Important Takeaways")

        for takeaway in summary["takeaways"]:
            st.write(f"• {takeaway}")
        st.subheader("Timestamped Transcript")

        for item in transcript_data:
            st.markdown(
                f"**[{seconds_to_time(item['start'])} - {seconds_to_time(item['end'])}]** {item['text']}"
            )
