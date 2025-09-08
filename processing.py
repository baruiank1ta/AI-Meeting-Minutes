
import streamlit as st
from huggingface_hub import InferenceClient
from faster_whisper import WhisperModel
from fpdf import FPDF
import time


@st.cache_resource
def load_whisper_model():
    """
    Loads the faster-whisper model. The @st.cache_resource decorator
    ensures this model is loaded only once.
    """
    try:
        model = WhisperModel("base", device="cpu", compute_type="int8")
        return model
    except Exception as e:
        st.error(f"Error loading Whisper model: {e}")
        return None

def create_pdf(text_content):
    """
    Creates a PDF file in memory from the provided text content.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    
    # Add a title
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, 'AI-Generated Meeting Minutes', 0, 1, 'C')
    pdf.ln(10) # Add a little space

    # Reset font for the content
    pdf.set_font("Helvetica", size=12)
    
    encoded_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, encoded_text)
    
    # Explicitly convert the output to 'bytes' to satisfy Streamlit's strict type requirement.
    return bytes(pdf.output())

def transcribe_audio(audio_file_path, whisper_model):
    """
    Transcribes the audio file silently in the background.
    """
    try:
        segments, info = whisper_model.transcribe(audio_file_path, beam_size=5)
        full_transcript = ""
        for segment in segments:
            full_transcript += segment.text + " "
        return full_transcript.strip()
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        return None

def generate_minutes_with_hf_llm(api_key, transcript):
    """
    Analyzes the transcript using a powerful open-source model hosted on Hugging Face.
    """
    try:
        client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=api_key)
        prompt_messages = [{"role": "user", "content": f"""You are an expert assistant skilled at creating meeting minutes. Analyze the following transcript and provide a structured summary in Markdown with three sections: 'Executive Summary', 'Key Discussion Points', and 'Action Items'. For action items, assign the task to the correct person.

                Here is the transcript:
                ---
                {transcript}
                ---
                """}]
        response_stream = client.chat_completion(messages=prompt_messages, max_tokens=2048, stream=False)
        return response_stream.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the Hugging Face API: {str(e)}"