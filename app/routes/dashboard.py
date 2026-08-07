"""
app/routes/dashboard.py — Dashboard Blueprint
================================================
Why this file exists:
    Serves the dynamic dashboard — the main page users see after login.
    Gathers stats (total conversations, career matches, recent activity)
    and passes them to Jinja2 templates. Also provides a JSON endpoint
    for client-side Chart.js to fetch data asynchronously.
"""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from ..extensions import db
from ..models.conversation import Conversation, Message
from ..models.career import Career

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """Render the main dashboard with summary statistics."""
    # ── Gather Stats ────────────────────────────────────
    total_conversations = Conversation.query.filter_by(
        user_id=current_user.id
    ).count()

    total_messages = (
        db.session.query(Message)
        .join(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .count()
    )

    total_careers = Career.query.count()

    recent_conversations = (
        Conversation.query
        .filter_by(user_id=current_user.id)
        .order_by(Conversation.updated_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'dashboard/index.html',
        total_conversations=total_conversations,
        total_messages=total_messages,
        total_careers=total_careers,
        recent_conversations=recent_conversations,
    )


@dashboard_bp.route('/stats')
@login_required
def stats():
    """Return dashboard chart data as JSON (consumed by dashboard.js)."""
    # Messages per day (last 7 days) — example aggregation
    conversations = (
        Conversation.query
        .filter_by(user_id=current_user.id)
        .order_by(Conversation.created_at.desc())
        .limit(10)
        .all()
    )

    return jsonify({
        'conversations': [c.to_dict() for c in conversations],
        'total_careers': Career.query.count(),
    })
