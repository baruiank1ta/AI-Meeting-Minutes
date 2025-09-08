#AI-Powered Meeting Minutes Generator

This project is a web app that automates the boring part of meetings — writing the minutes.
Give it an audio recording, and it will transcribe, analyze, and generate a clean, professional summary with action items. You can also paste in raw transcripts if you already have them. The goal is simple: spend less time typing notes, and more time actually doing the work.


✨ Features

🎙️ Audio-to-Text: Upload .mp3, .wav, or .m4a files for accurate transcription.

📝 Transcript Input: Already have notes? Just paste them in.

🤖 Smart AI Analysis: Generates three sections:
            Executive summary
            Key discussion points
            Action items (with clear responsibilities)


📄 Export: Download a polished PDF report instantly.

🔒 Secure API Management: Keep tokens safe with Streamlit’s built-in secrets system.


🛠️ Tech Stack

Frontend/UI: Streamlit

Backend & Logic: Python

Transcription: faster-whisper

AI Model: Meta-Llama-3-8B-Instruct (via Hugging Face)

PDF Export: fpdf2
