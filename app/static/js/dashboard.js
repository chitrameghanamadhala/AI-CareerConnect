/**
 * static/js/dashboard.js — Dashboard Charts & Real-Time Updates
 * ===============================================================
 * Why this file exists:
 *   Powers the dynamic dashboard by:
 *   1. Fetching stats data from /dashboard/stats (JSON)
 *   2. Rendering Chart.js visualizations
 *   3. Enabling live updates without full page reloads
 *
 *   Only loaded on the dashboard page (via extra_js block).
 */

'use strict';

document.addEventListener('DOMContentLoaded', () => {
    initDashboardChart();
});


async function initDashboardChart() {
    const canvas = document.getElementById('career-chart');
    if (!canvas) return;

    try {
        const data = await apiFetch('/dashboard/stats');
        renderConversationChart(canvas, data.conversations);
    } catch (error) {
        console.warn('Could not load dashboard data:', error.message);
        renderEmptyChart(canvas);
    }
}


function renderConversationChart(canvas, conversations) {
    const labels = conversations.map((c) => c.title.substring(0, 20));
    const messageCounts = conversations.map((c) => c.message_count);

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels.length ? labels : ['No data yet'],
            datasets: [{
                label: 'Messages per Conversation',
                data: messageCounts.length ? messageCounts : [0],
                backgroundColor: 'rgba(99, 102, 241, 0.6)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 1,
                borderRadius: 6,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94a3b8', font: { family: 'Inter' } },
                },
            },
            scales: {
                x: {
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(51, 65, 85, 0.5)' },
                },
                y: {
                    ticks: { color: '#94a3b8', stepSize: 1 },
                    grid: { color: 'rgba(51, 65, 85, 0.5)' },
                    beginAtZero: true,
                },
            },
        },
    });
}


function renderEmptyChart(canvas) {
    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: ['Start chatting!'],
            datasets: [{
                label: 'Messages',
                data: [0],
                backgroundColor: 'rgba(99, 102, 241, 0.3)',
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        },
    });
}
