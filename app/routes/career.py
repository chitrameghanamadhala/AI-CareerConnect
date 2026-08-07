"""
app/routes/career.py — Career Blueprint
=========================================
Why this file exists:
    Handles career browsing, recommendation display, and detail views.
    Separated from the dashboard so career-specific logic (filtering,
    searching, AI-driven recommendations) doesn't bloat the main
    dashboard blueprint.
"""

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ..models.career import Career
from ..services.career_analyzer import CareerAnalyzer

career_bp = Blueprint('career', __name__, url_prefix='/career')


@career_bp.route('/recommendations')
@login_required
def recommendations():
    """Show AI-generated career recommendations."""
    # Fetch user's skills/interests from recent conversations
    analyzer = CareerAnalyzer()
    recommended = analyzer.get_recommendations(current_user.id)

    return render_template(
        'career/recommendations.html',
        careers=recommended,
    )


@career_bp.route('/<int:career_id>')
@login_required
def detail(career_id):
    """Show detailed info about a specific career path."""
    career = Career.query.get_or_404(career_id)
    return render_template('career/detail.html', career=career)


@career_bp.route('/search')
@login_required
def search():
    """Search careers by keyword."""
    query = request.args.get('q', '').strip()
    results = []
    if query:
        results = Career.query.filter(
            Career.title.ilike(f'%{query}%')
            | Career.description.ilike(f'%{query}%')
        ).all()

    return render_template(
        'career/recommendations.html',
        careers=results,
        search_query=query,
    )
