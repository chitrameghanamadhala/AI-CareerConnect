/**
 * static/js/app.js — Core Application JavaScript
 * =================================================
 * Why this file exists:
 *   Shared JS utilities used across all pages. Handles:
 *   - Auto-dismissal of flash messages
 *   - CSRF token extraction for AJAX requests
 *   - Utility functions (fetch wrappers, formatters)
 *
 *   Page-specific JS lives in dashboard.js, chat.js, speech.js.
 */

'use strict';

// ── Auto-dismiss Flash Messages (after 5 seconds) ──
document.addEventListener('DOMContentLoaded', () => {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach((flash) => {
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-10px)';
            setTimeout(() => flash.remove(), 300);
        }, 5000);
    });
});

// ── Fetch Wrapper (handles JSON + errors) ───────────
async function apiFetch(url, options = {}) {
    const defaults = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = { ...defaults, ...options };
    if (options.headers) {
        config.headers = { ...defaults.headers, ...options.headers };
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `HTTP ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error(`API Error [${url}]:`, error.message);
        throw error;
    }
}

// ── Format Numbers ──────────────────────────────────
function formatNumber(num) {
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M';
    if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K';
    return num.toString();
}

// ── Debounce ────────────────────────────────────────
function debounce(func, delay = 300) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), delay);
    };
}
