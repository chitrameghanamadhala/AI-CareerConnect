"""
app/services/speech_to_text.py — Speech-to-Text Service
=========================================================
Why this file exists:
    Converts audio input (recorded in the browser) to text. This is a
    SERVER-SIDE service that receives audio blobs via the /api/speech-to-text
    endpoint. The actual recording happens in the browser (speech.js).

    Decoupled from routes so the STT engine can be swapped (Whisper,
    Google Speech API, Azure) without changing any route code.

    Current implementation: SpeechRecognition library with Google's
    free web API. For production, consider Whisper or a paid API.
"""

import os
import tempfile
from flask import current_app

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False


def transcribe_audio(audio_file):
    """
    Transcribe an uploaded audio file to text.

    Args:
        audio_file: A FileStorage object (from Flask request.files).

    Returns:
        str: Transcribed text, or an error message.
    """
    if not SR_AVAILABLE:
        return "[Speech Recognition library not installed. Run: pip install SpeechRecognition]"

    recognizer = sr.Recognizer()

    # Save uploaded file to a temp location
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix='.wav', delete=False
        ) as temp_file:
            audio_file.save(temp_file)
            temp_path = temp_file.name

        # ── Transcribe ──────────────────────────────────
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(
            audio_data,
            language=current_app.config.get('SPEECH_LANGUAGE', 'en'),
        )
        return text

    except sr.UnknownValueError:
        return "[Could not understand the audio. Please try again.]"
    except sr.RequestError as e:
        current_app.logger.error(f'STT API error: {e}')
        return f"[Speech recognition service error: {e}]"
    except Exception as e:
        current_app.logger.error(f'STT error: {e}')
        return f"[Transcription error: {e}]"
    finally:
        # Clean up temp file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
