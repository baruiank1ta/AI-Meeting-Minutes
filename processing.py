import streamlit as st
from groq import Groq
from faster_whisper import WhisperModel
from fpdf import FPDF


@st.cache_resource
def load_whisper_model():
    """
    Loads the faster-whisper model only once.
    """
    try:
        model = WhisperModel("base", device="cpu", compute_type="int8")
        return model
    except Exception as e:
        st.error(f"Error loading Whisper model: {e}")
        return None


def create_pdf(text_content):
    """
    Creates a PDF file in memory from text content.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "AI-Generated Meeting Minutes", 0, 1, "C")
    pdf.ln(10)

    pdf.set_font("Helvetica", size=12)
    encoded_text = text_content.encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 10, encoded_text)

    return bytes(pdf.output())


def transcribe_audio(audio_file_path, whisper_model):
    """
    Transcribes audio file.
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


def generate_minutes_with_llm(api_key, transcript):
    """
    Generates structured meeting minutes using Groq LLM.
    """
    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional assistant skilled at generating structured meeting minutes."
                },
                {
                    "role": "user",
                    "content": f"""
Generate well-structured meeting minutes from the transcript below.

Include:
- Key discussion points
- Decisions made
- Action items
- Summary

Transcript:
{transcript}
"""
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"An error occurred with the Groq API: {str(e)}"

