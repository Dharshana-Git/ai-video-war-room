"""
AI Video Marketing War Room - Main Application
A production-grade competitive intelligence platform for YouTube marketing analysis.
"""

import streamlit as st
import time
from youtube_service import YouTubeService
from analytics_engine import AnalyticsEngine
from ui_components import (
    render_header, render_input_section, render_executive_summary,
    render_channel_intelligence, render_engagement_intelligence,
    render_aei_analysis, render_content_themes, render_viral_patterns,
    render_whitespace_map, render_threat_scoring, render_ai_recommendations,
    render_content_roadmap, inject_custom_css
)
from ppt_generator import generate_ppt_report
from utils import validate_inputs, show_error, show_success

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Marketing War Room",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_custom_css()


def main():
    render_header()

    # ─── Session State Init ──────────────────────────────────────────────────
    if "analysis_done" not in st.session_state:
        st.session_state.analysis_done = False
    if "channel_data" not in st.session_state:
        st.session_state.channel_data = {}
    if "analytics" not in st.session_state:
        st.session_state.analytics = None

    # ─── Input Section ───────────────────────────────────────────────────────
    user_company, competitors = render_input_section()

    col_btn, col_reset = st.columns([3, 1])
    with col_btn:
        generate_clicked = st.button(
            "⚔️ Generate Intelligence Report",
            type="primary",
            use_container_width=True
        )
    with col_reset:
        if st.session_state.analysis_done:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.analysis_done = False
                st.session_state.channel_data = {}
                st.session_state.analytics = None
                st.rerun()

    # ─── Data Collection ─────────────────────────────────────────────────────
    if generate_clicked:
        all_companies = [user_company] + [c for c in competitors if c.strip()]
        valid, msg = validate_inputs(user_company, competitors)
        if not valid:
            show_error(msg)
            return

        try:
            # st.secrets supports both dict-style and attribute access
            youtube_api_key = st.secrets["YOUTUBE_API_KEY"]
        except Exception:
            youtube_api_key = ""
        try:
            gemini_api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            gemini_api_key = ""

        if not youtube_api_key:
            st.warning("⚠️ No YouTube API key found in secrets.toml. Running in demo mode with simulated data.")

        with st.spinner(""):
            progress_bar = st.progress(0)
            status = st.empty()

            channel_data = {}
            yt_service = YouTubeService(youtube_api_key)

            for i, company in enumerate(all_companies):
                status.markdown(
                    f'<div class="status-pill">🔍 Fetching intelligence for <strong>{company}</strong>...</div>',
                    unsafe_allow_html=True
                )
                progress_bar.progress((i) / len(all_companies))

                data = yt_service.fetch_channel_data(company)
                if data:
                    channel_data[company] = data
                time.sleep(0.3)

            progress_bar.progress(1.0)
            status.markdown(
                '<div class="status-pill">🧠 Running AI analysis engine...</div>',
                unsafe_allow_html=True
            )
            time.sleep(0.5)

            analytics = AnalyticsEngine(channel_data, user_company, gemini_api_key)
            analytics.run_full_analysis()

            st.session_state.channel_data = channel_data
            st.session_state.analytics = analytics
            st.session_state.user_company = user_company
            st.session_state.analysis_done = True

            progress_bar.empty()
            status.empty()
            show_success(f"Intelligence report generated for {len(channel_data)} companies.")

    # ─── Dashboard ────────────────────────────────────────────────────────────
    if st.session_state.analysis_done and st.session_state.analytics:
        analytics = st.session_state.analytics
        channel_data = st.session_state.channel_data
        user_company = st.session_state.get("user_company", list(channel_data.keys())[0])

        st.markdown("---")

        tabs = st.tabs([
            "📊 Executive Summary",
            "📡 Channel Intelligence",
            "💥 Engagement",
            "🎯 AEI Index",
            "🎨 Content Themes",
            "🔥 Viral Patterns",
            "🗺️ White Space Map",
            "⚠️ Threat Scoring",
            "🤖 AI Recommendations",
            "📅 30-Day Roadmap"
        ])

        with tabs[0]:
            render_executive_summary(analytics, channel_data, user_company)
        with tabs[1]:
            render_channel_intelligence(analytics, channel_data)
        with tabs[2]:
            render_engagement_intelligence(analytics, channel_data)
        with tabs[3]:
            render_aei_analysis(analytics, channel_data)
        with tabs[4]:
            render_content_themes(analytics, channel_data)
        with tabs[5]:
            render_viral_patterns(analytics, channel_data)
        with tabs[6]:
            render_whitespace_map(analytics, channel_data, user_company)
        with tabs[7]:
            render_threat_scoring(analytics, channel_data)
        with tabs[8]:
            render_ai_recommendations(analytics, user_company)
        with tabs[9]:
            render_content_roadmap(analytics, user_company)

        # ─── PPT Export ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📥 Export Intelligence Report")
        col1, col2 = st.columns([2, 3])
        with col1:
            if "ppt_bytes" not in st.session_state:
                st.session_state.ppt_bytes = None

            if st.button("🎯 Generate PowerPoint Report", use_container_width=True):
                with st.spinner("Building your premium intelligence deck..."):
                    st.session_state.ppt_bytes = generate_ppt_report(analytics, channel_data, user_company)

            if st.session_state.ppt_bytes:
                st.download_button(
                    label="⬇️ Download Intelligence Report (.pptx)",
                    data=st.session_state.ppt_bytes,
                    file_name=f"AI_War_Room_{user_company.replace(' ', '_')}.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True
                )
        with col2:
            st.info("📋 Your report includes 12 slides: Executive Summary, Channel Intelligence, Engagement Analysis, AEI Scores, Content Strategy, Threat Matrix, and a 30-Day Roadmap.")


if __name__ == "__main__":
    main()
