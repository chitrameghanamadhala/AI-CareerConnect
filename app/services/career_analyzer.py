"""
app/services/career_analyzer.py — Career Analysis Service
============================================================
Why this file exists:
    Contains the business logic for matching users to career paths.
    Analyzes conversation history and user data to generate personalized
    career recommendations. This keeps the recommendation algorithm
    testable and separate from route handling.
"""

from flask import current_app
from ..extensions import db
from ..models.career import Career
from ..models.conversation import Conversation, Message


class CareerAnalyzer:
    """Analyzes user data and suggests matching career paths."""

    def get_recommendations(self, user_id, limit=5):
        """
        Generate career recommendations based on user's conversation history.

        Args:
            user_id: The ID of the user.
            limit: Maximum number of recommendations to return.

        Returns:
            list[Career]: Recommended career objects.
        """
        # ── Extract Keywords from User Messages ────────
        user_messages = (
            db.session.query(Message.content)
            .join(Conversation)
            .filter(
                Conversation.user_id == user_id,
                Message.role == 'user',
            )
            .all()
        )

        keywords = self._extract_keywords(user_messages)

        # ── Match Against Career Database ──────────────
        if keywords:
            careers = self._search_careers(keywords, limit)
        else:
            # Fallback: return top careers by growth rate
            careers = (
                Career.query
                .order_by(Career.growth_rate.desc())
                .limit(limit)
                .all()
            )

        return careers

    def _extract_keywords(self, messages):
        """
        Extract relevant keywords from user message history.

        Args:
            messages: List of (content,) tuples from the DB query.

        Returns:
            list[str]: Extracted keywords.
        """
        keywords = []
        # Simple keyword extraction — upgrade to NLP/Mistral in production
        stop_words = {'i', 'am', 'a', 'the', 'is', 'in', 'it', 'to', 'and', 'of'}

        for (content,) in messages:
            words = content.lower().split()
            keywords.extend(
                w for w in words
                if len(w) > 3 and w not in stop_words
            )

        return list(set(keywords))[:20]  # deduplicate, cap at 20

    def _search_careers(self, keywords, limit):
        """
        Search careers matching any of the given keywords.

        Args:
            keywords: List of keyword strings.
            limit: Max results.

        Returns:
            list[Career]: Matching career objects.
        """
        query = Career.query
        filters = [
            Career.title.ilike(f'%{kw}%') | Career.description.ilike(f'%{kw}%')
            for kw in keywords[:5]  # limit filter complexity
        ]

        if filters:
            from sqlalchemy import or_
            query = query.filter(or_(*filters))

        return query.limit(limit).all()
