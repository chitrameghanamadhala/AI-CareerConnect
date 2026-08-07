"""
app/services/mistral_service.py — Mistral AI Integration
==========================================================
Why this file exists:
    Encapsulates ALL interaction with the Mistral AI API in one place.
    Routes call `MistralService.chat()` — they never see HTTP clients,
    token counts, or prompt templates. If you switch to a different LLM
    (OpenAI, Gemini), you only change THIS file.

    Responsibilities:
    - Build system prompts for career guidance
    - Send multi-turn conversation history to Mistral
    - Handle API errors gracefully
    - Manage token limits
"""

import os
from flask import current_app
from mistralai import Mistral


# ── System Prompt ───────────────────────────────────────
CAREER_SYSTEM_PROMPT = """You are AI Career Connect, an expert career guidance counselor.
Your role is to:
1. Understand the user's skills, interests, education, and experience.
2. Suggest suitable career paths with clear reasoning.
3. Recommend skills to learn and resources for growth.
4. Provide salary insights, job market trends, and growth potential.
5. Be encouraging, specific, and actionable in your advice.

Always structure your responses with clear headings and bullet points
when listing multiple items. Keep responses concise but thorough."""


class MistralService:
    """Wrapper around the Mistral AI chat completions API."""

    def __init__(self):
        api_key = current_app.config.get('MISTRAL_API_KEY') or os.getenv('MISTRAL_API_KEY', '')
        self.model = current_app.config.get('MISTRAL_MODEL', 'mistral-large-latest')
        self.client = Mistral(api_key=api_key) if api_key else None

    def chat(self, messages, temperature=0.7, max_tokens=1024):
        """
        Send a conversation to Mistral and return the assistant's reply.

        Args:
            messages: List of dicts with 'role' and 'content' keys.
            temperature: Creativity control (0.0 = deterministic, 1.0 = creative).
            max_tokens: Maximum response length.

        Returns:
            str: The AI's response text.
        """
        if not self.client:
            return (
                "⚠️ Mistral API key not configured. "
                "Please set MISTRAL_API_KEY in your .env file."
            )

        # Prepend system prompt
        full_messages = [
            {'role': 'system', 'content': CAREER_SYSTEM_PROMPT},
            *messages,
        ]

        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=full_messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content

        except Exception as e:
            current_app.logger.error(f'Mistral API error: {e}')
            return f"Sorry, I encountered an error: {str(e)}"

    def analyze_skills(self, user_text):
        """
        Extract skills and interests from free-form user text.

        Returns:
            str: Structured analysis of detected skills.
        """
        prompt = (
            f"Analyze the following text and extract:\n"
            f"1. Technical skills\n"
            f"2. Soft skills\n"
            f"3. Career interests\n"
            f"4. Experience level\n\n"
            f"Text: {user_text}\n\n"
            f"Respond in JSON format."
        )
        return self.chat([{'role': 'user', 'content': prompt}])
