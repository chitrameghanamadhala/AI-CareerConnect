/**
 * static/js/chat.js — AI Chat Interface
 * =======================================
 * Why this file exists:
 *   Handles the client-side logic for the AI chat widget:
 *   - Sends user messages to /api/chat via AJAX
 *   - Displays user and AI messages in the chat window
 *   - Triggers TTS playback for AI responses
 *   - Manages conversation state (conversation_id)
 *
 *   Works alongside speech.js for voice input.
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
    const chatInput = document.getElementById('chat-input');
    const btnSend = document.getElementById('btn-send');
    const chatMessages = document.getElementById('chat-messages');

    if (!chatInput || !btnSend || !chatMessages) return;

    let conversationId = null;

    // ── Send on Button Click ────────────────────────────
    btnSend.addEventListener('click', () => sendMessage());

    // ── Send on Enter Key ───────────────────────────────
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });


    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Show user message
        appendMessage('user', text);
        chatInput.value = '';
        btnSend.disabled = true;

        // Show typing indicator
        const typingEl = appendMessage('assistant', '⏳ Thinking...');

        try {
            const data = await apiFetch('/api/chat', {
                method: 'POST',
                body: JSON.stringify({
                    message: text,
                    conversation_id: conversationId,
                }),
            });

            conversationId = data.conversation_id;
            typingEl.querySelector('p').textContent = data.reply;

            // Auto-play TTS for AI response (optional)
            requestTTS(data.reply);

        } catch (error) {
            typingEl.querySelector('p').textContent =
                '❌ Error: Could not reach the AI. Please try again.';
        } finally {
            btnSend.disabled = false;
            chatInput.focus();
        }
    }


    function appendMessage(role, content) {
        const div = document.createElement('div');
        div.className = `chat-message ${role}`;
        div.innerHTML = `<p>${escapeHtml(content)}</p>`;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return div;
    }


    async function requestTTS(text) {
        try {
            const data = await apiFetch('/api/text-to-speech', {
                method: 'POST',
                body: JSON.stringify({ text }),
            });

            if (data.audio_url) {
                const audio = document.getElementById('tts-audio');
                audio.src = data.audio_url;
                // Don't auto-play — user can click speaker icon
            }
        } catch (error) {
            console.warn('TTS error:', error.message);
        }
    }


    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Expose for speech.js to call
    window.sendChatMessage = function(text) {
        chatInput.value = text;
        sendMessage();
    };
});
