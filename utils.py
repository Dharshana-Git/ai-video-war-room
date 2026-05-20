"""
utils.py — Shared utility functions for validation, formatting, and UI helpers.
"""

import streamlit as st


def validate_inputs(user_company: str, competitors: list) -> tuple[bool, str]:
    """Validate that at least 1 competitor and a user company are provided."""
    if not user_company or not user_company.strip():
        return False, "Please enter your company name."

    filled_competitors = [c for c in competitors if c and c.strip()]
    if len(filled_competitors) < 1:
        return False, "Please enter at least one competitor company name."

    if len(user_company.strip()) > 80:
        return False, "Company name is too long (max 80 characters)."

    return True, ""


def show_error(msg: str):
    st.markdown(f"""
    <div style="
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 3px solid #ef4444;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        color: #fca5a5;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    ">
        ❌ {msg}
    </div>
    """, unsafe_allow_html=True)


def show_success(msg: str):
    st.markdown(f"""
    <div style="
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-left: 3px solid #10b981;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        color: #6ee7b7;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    ">
        ✅ {msg}
    </div>
    """, unsafe_allow_html=True)


def format_large_number(n: float) -> str:
    """Format large numbers as K/M abbreviations."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(int(n))


def get_color_for_score(score: float) -> str:
    """Return a hex color based on a 0–10 score."""
    if score >= 7:
        return "#10b981"
    elif score >= 4:
        return "#f59e0b"
    return "#ef4444"
