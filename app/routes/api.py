"""
app/routes/api.py — REST API Blueprint
========================================
Why this file exists:
    Provides JSON-only endpoints consumed by the frontend JavaScript.
    This includes the AI chat endpoint (sends user messages to Mistral),
    speech-to-text upload, and text-to-speech generation. Keeping API
    routes separate from page-rendering routes gives a clean separation
    between server-rendered HTML and client-side AJAX calls.
"""

import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from ..extensions import db
from ..models.conversation import Conversation, Message
from ..services.mistral_service import MistralService
from ..services.speech_to_text import transcribe_audio
from ..services.text_to_speech import synthesize_speech

api_bp = Blueprint('api', __name__)


@api_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """
    Send a user message to Mistral AI and return the response.

    Expects JSON: { "message": "...", "conversation_id": int|null }
    Returns JSON: { "reply": "...", "conversation_id": int }
    """
    data = request.get_json(silent=True) or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Message is required.'}), 400

    # ── Get or Create Conversation ──────────────────────
    conv_id = data.get('conversation_id')
    if conv_id:
        conversation = Conversation.query.get(conv_id)
    else:
        conversation = Conversation(
            user_id=current_user.id,
            title=user_message[:50],
        )
        db.session.add(conversation)
        db.session.flush()  # get the ID before committing

    # ── Save User Message ──────────────────────────────
    user_msg = Message(
        conversation_id=conversation.id,
        role='user',
        content=user_message,
    )
    db.session.add(user_msg)

    # ── Call Mistral AI ─────────────────────────────────
    mistral = MistralService()
    history = [
        {'role': m.role, 'content': m.content}
        for m in conversation.messages.all()
    ]
    history.append({'role': 'user', 'content': user_message})

    ai_reply = mistral.chat(history)

    # ── Save AI Response ────────────────────────────────
    ai_msg = Message(
        conversation_id=conversation.id,
        role='assistant',
        content=ai_reply,
    )
    db.session.add(ai_msg)
    db.session.commit()

    return jsonify({
        'reply': ai_reply,
        'conversation_id': conversation.id,
    })


@api_bp.route('/speech-to-text', methods=['POST'])
@login_required
def speech_to_text():
    """
    Receive an audio file and return transcribed text.

    Expects: multipart/form-data with an 'audio' file.
    Returns JSON: { "text": "transcribed text" }
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided.'}), 400

    audio_file = request.files['audio']
    text = transcribe_audio(audio_file)

    return jsonify({'text': text})


@api_bp.route('/text-to-speech', methods=['POST'])
@login_required
def text_to_speech():
    """
    Convert text to speech audio.

    Expects JSON: { "text": "..." }
    Returns JSON: { "audio_url": "/static/audio/xxx.mp3" }
    """
    data = request.get_json(silent=True) or {}
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'Text is required.'}), 400

    audio_path = synthesize_speech(text)
    audio_url = f'/static/audio/{os.path.basename(audio_path)}'

    return jsonify({'audio_url': audio_url})
