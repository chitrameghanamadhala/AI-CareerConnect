"""
app/services/text_to_speech.py — Text-to-Speech Service
=========================================================
Why this file exists:
    Converts AI text responses into audio files so users can LISTEN to
    career advice. Uses gTTS (Google Text-to-Speech) to generate MP3s
    and caches them in `static/audio/` to avoid re-synthesis of
    identical text.

    Decoupled from routes — if you switch to pyttsx3 (offline) or
    Amazon Polly (premium), only THIS file changes.
"""

import os
import hashlib
from flask import current_app

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


def synthesize_speech(text, language='en'):
    """
    Convert text to an MP3 audio file.

    Args:
        text: The text to convert to speech.
        language: Language code (default: 'en').

    Returns:
        str: Absolute path to the generated audio file.
    """
    audio_dir = current_app.config.get(
        'TTS_AUDIO_DIR',
        os.path.join('app', 'static', 'audio'),
    )
    os.makedirs(audio_dir, exist_ok=True)

    # ── Cache Key (hash of text) ────────────────────────
    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:12]
    filename = f'tts_{text_hash}.mp3'
    filepath = os.path.join(audio_dir, filename)

    # Return cached file if it exists
    if os.path.exists(filepath):
        return filepath

    if not GTTS_AVAILABLE:
        current_app.logger.warning('gTTS not installed. Run: pip install gTTS')
        return ''

    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filepath)
        current_app.logger.info(f'TTS audio saved: {filename}')
        return filepath

    except Exception as e:
        current_app.logger.error(f'TTS error: {e}')
        return ''
