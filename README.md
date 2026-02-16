# AI-Powered Meeting Minutes Generator

This project is a web app that automates the boring part of meetings — writing the minutes.
Give it an audio recording, and it will transcribe, analyze, and generate a clean, professional summary with action items. You can also paste in raw transcripts if you already have them. The goal is simple: spend less time typing notes, and more time actually doing the work.

Give it an audio recording, and it will:

🎙 Transcribe the audio

🧠 Analyze the discussion

📝 Generate clean, structured meeting minutes

📄 Export a polished PDF report

You can also paste an existing transcript directly and generate minutes instantly.

The goal is simple:
Spend less time writing notes, more time making decisions.


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

AI Model: Llama-3.1-8B-Instant, Hosted via Groq API (high-speed inference)

PDF Export: fpdf2


⚙️ How It Works

Audio is uploaded to the app.

Faster-Whisper transcribes it into text.

The transcript is sent to Groq’s Llama 3.1 model.

The model generates structured meeting minutes.

The result can be downloaded as a formatted PDF.


* Live Demo:https://ai-meeting-minutes-vwhj694qkvfeat8mjmyhbe.streamlit.app
