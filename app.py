import streamlit as st
import processing
import os
import time

# --- Page Config ---
st.set_page_config(layout="wide")
st.title("📋 AI-Powered Meeting Minutes Generator")

# --- Load Whisper Model ---
whisper_model = processing.load_whisper_model()
if whisper_model is None:
    st.stop()

# --- Get Groq API Key from Streamlit Secrets ---
try:
    api_key_input = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Groq API key not found. Please add it to Streamlit secrets.")
    st.stop()

# --- UI Tabs ---
tab1, tab2 = st.tabs([
    "🎙 Transcribe Audio & Generate Minutes",
    "📝 Generate Minutes from Text"
])

# ==========================
# TAB 1: AUDIO UPLOAD
# ==========================
with tab1:
    st.header("Upload an Audio File")
    st.markdown(
        "Upload a meeting recording (`.mp3`, `.wav`, `.m4a`). "
        "The AI will transcribe it and generate structured minutes."
    )

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["mp3", "wav", "m4a", "m4b"]
    )

    if uploaded_file is not None:
        if st.button("Transcribe and Generate Minutes"):
            with st.spinner("Processing audio..."):

                # Save temp file
                temp_file_path = f"temp_{uploaded_file.name}"
                with open(temp_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Transcribe
                transcript = processing.transcribe_audio(
                    temp_file_path,
                    whisper_model
                )

                os.remove(temp_file_path)

            if transcript:
                with st.expander("View Full Transcript"):
                    st.text_area("Transcript", transcript, height=200)

                with st.spinner("Generating meeting minutes..."):
                    llm_output = processing.generate_minutes_with_llm(
                        api_key_input,
                        transcript
                    )

                st.subheader("📝 Generated Meeting Minutes")
                st.markdown(llm_output)

                if llm_output and not llm_output.startswith("An error occurred"):
                    pdf_bytes = processing.create_pdf(llm_output)
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_bytes,
                        file_name=f"meeting_minutes_{int(time.time())}.pdf",
                        mime="application/pdf"
                    )

# ==========================
# TAB 2: TEXT INPUT
# ==========================
with tab2:
    st.header("Paste Your Transcript")
    transcript_input = st.text_area(
        "Paste Full Transcript Here",
        height=300
    )

    if st.button("Generate Minutes from Text"):
        if not transcript_input.strip():
            st.warning("Please paste a transcript.")
        else:
            with st.spinner("Generating meeting minutes..."):
                llm_output = processing.generate_minutes_with_llm(
                    api_key_input,
                    transcript_input
                )

            st.subheader("📝 Generated Meeting Minutes")
            st.markdown(llm_output)

            if llm_output and not llm_output.startswith("An error occurred"):
                pdf_bytes = processing.create_pdf(llm_output)
                st.download_button(
                    label="Download as PDF",
                    data=pdf_bytes,
                    file_name=f"meeting_minutes_{int(time.time())}.pdf",
                    mime="application/pdf"
                )
