
import streamlit as st
import processing  # Import our new toolbox of helper functions
import os
import time

# --- Streamlit User Interface ---

st.set_page_config(layout="wide")
st.title("📋 AI-Powered Meeting Minutes Generator")

# Load the model by calling the function from processing.py
whisper_model = processing.load_whisper_model()
if whisper_model is None:
    st.stop()

# API Key Management
api_key_input = None
if st.secrets.get("HF_API_TOKEN"):
    api_key_input = st.secrets["HF_API_TOKEN"]
else:
    st.markdown("Get your free Hugging Face access token from [your HF settings](https://huggingface.co/settings/tokens).")
    api_key_input = st.text_input("Enter your Hugging Face Access Token:", type="password", help="To avoid entering this every time, create a file at .streamlit/secrets.toml with your key.")

# --- UI Tabs for different workflows ---
tab1, tab2 = st.tabs(["**Transcribe Audio & Generate Minutes**", "**Generate Minutes from Text**"])

with tab1:
    st.header("Upload an Audio File")
    st.markdown("Upload an audio recording of your meeting (`.mp3`, `.wav`, `.m4a`). The AI will transcribe it and generate the minutes.")
    uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "m4b"])

    if uploaded_file is not None:
        if st.button("Transcribe and Generate Minutes"):
            if not api_key_input:
                st.error("API Key is missing. Please enter your key above or add it to a .streamlit/secrets.toml file.")
            else:
                with st.spinner("Processing audio... This may take a few moments depending on the file size."):
                    with open(uploaded_file.name, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Call the function from processing.py
                    transcript = processing.transcribe_audio(uploaded_file.name, whisper_model)
                    
                    os.remove(uploaded_file.name)
                
                if transcript:
                    with st.expander("View Full Transcript"):
                        st.text_area("Transcript", transcript, height=200)

                    with st.spinner("The AI is analyzing the transcript..."):
                        # Call the function from processing.py
                        llm_output = processing.generate_minutes_with_hf_llm(api_key_input, transcript)
                        st.subheader("📝 Generated Meeting Minutes")
                        st.markdown(llm_output)

                        if llm_output and not llm_output.startswith("An error occurred"):
                            # Call the function from processing.py
                            pdf_bytes = processing.create_pdf(llm_output)
                            st.download_button(
                                label="Download as PDF",
                                data=pdf_bytes,
                                file_name=f"meeting_minutes_{int(time.time())}.pdf",
                                mime="application/pdf"
                            )

with tab2:
    st.header("Paste Your Transcript")
    st.markdown("If you already have a transcript, paste it here to generate the minutes directly.")
    transcript_input = st.text_area("Paste Full Transcript Here", height=300, key="text_input")

    if st.button("Generate Minutes from Text"):
        if not api_key_input:
            st.error("API Key is missing. Please enter your key above or add it to a .streamlit/secrets.toml file.")
        elif not transcript_input.strip():
            st.warning("Please paste a transcript to generate minutes.")
        else:
            with st.spinner("The AI is analyzing the transcript..."):
                # Call the function from processing.py
                llm_output = processing.generate_minutes_with_hf_llm(api_key_input, transcript_input)
                st.subheader("📝 Generated Meeting Minutes")
                st.markdown(llm_output)

                if llm_output and not llm_output.startswith("An error occurred"):
                    # Call the function from processing.py
                    pdf_bytes = processing.create_pdf(llm_output)
                    st.download_button(
                        label="Download as PDF",
                        data=pdf_bytes,
                        file_name=f"meeting_minutes_{int(time.time())}.pdf",
                        mime="application/pdf"
                    )