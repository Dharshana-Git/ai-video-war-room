"""
ui_components.py — All Streamlit UI rendering functions.
Premium SaaS dark theme with glassmorphism cards and Plotly charts.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from analytics_engine import AnalyticsEngine


# ─── CSS Injection ────────────────────────────────────────────────────────────

def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stApp {
        background: #080c14;
        color: #e2e8f0;
    }
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1400px;
    }

    /* ── Hide default streamlit elements ── */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }

    /* ── Header ── */
    .war-room-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .war-room-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(139, 92, 246, 0.08) 0%, transparent 60%),
                    radial-gradient(circle at 80% 20%, rgba(236, 72, 153, 0.06) 0%, transparent 50%);
        pointer-events: none;
    }
    .header-eyebrow {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        color: #8b5cf6;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .header-title {
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 30%, #a78bfa 70%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.5rem 0;
        line-height: 1.1;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        margin: 0;
    }
    .header-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.4);
        color: #a78bfa;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 8px;
        text-transform: uppercase;
    }

    /* ── Glass Card ── */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .glass-card-accent {
        background: rgba(139, 92, 246, 0.05);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    /* ── KPI Metric ── */
    .kpi-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .kpi-card:hover { border-color: rgba(139, 92, 246, 0.4); }
    .kpi-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #64748b;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f1f5f9;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.3rem;
    }
    .kpi-up { color: #34d399; }
    .kpi-down { color: #f87171; }

    /* ── Section Title ── */
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .section-subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    /* ── Insight Box ── */
    .insight-box {
        background: rgba(139, 92, 246, 0.08);
        border-left: 3px solid #8b5cf6;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        font-size: 0.9rem;
        color: #cbd5e1;
        line-height: 1.6;
    }
    .insight-box.green { border-left-color: #10b981; background: rgba(16, 185, 129, 0.06); }
    .insight-box.red { border-left-color: #ef4444; background: rgba(239, 68, 68, 0.06); }
    .insight-box.yellow { border-left-color: #f59e0b; background: rgba(245, 158, 11, 0.06); }

    /* ── Threat Score ── */
    .threat-bar-container { margin-bottom: 0.6rem; }
    .threat-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.82rem;
        color: #94a3b8;
        margin-bottom: 3px;
    }
    .threat-bar {
        height: 6px;
        border-radius: 3px;
        background: rgba(255,255,255,0.06);
        overflow: hidden;
    }
    .threat-bar-fill {
        height: 100%;
        border-radius: 3px;
        background: linear-gradient(90deg, #8b5cf6, #ec4899);
    }

    /* ── Status Pill ── */
    .status-pill {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 20px;
        padding: 0.5rem 1.2rem;
        text-align: center;
        color: #a78bfa;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }

    /* ── Roadmap Card ── */
    .roadmap-week {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .roadmap-week-title {
        font-size: 1rem;
        font-weight: 700;
        color: #a78bfa;
        margin-bottom: 0.75rem;
    }
    .roadmap-action {
        display: flex;
        align-items: flex-start;
        gap: 0.6rem;
        padding: 0.4rem 0;
        font-size: 0.88rem;
        color: #cbd5e1;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }
    .roadmap-goal {
        margin-top: 0.75rem;
        font-size: 0.8rem;
        color: #34d399;
        font-style: italic;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.02);
        border-radius: 10px;
        gap: 4px;
        padding: 4px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 500;
        padding: 0.5rem 0.8rem;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(139, 92, 246, 0.2) !important;
        color: #a78bfa !important;
    }

    /* ── Input Styling ── */
    .stTextInput input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: #f1f5f9 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    .stTextInput input:focus {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.3) !important;
    }

    /* ── Primary Button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7c3aed, #ec4899) !important;
        border: none !important;
        border-radius: 10px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        transition: all 0.2s !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
    }

    /* ── Plotly Chart bg ── */
    .js-plotly-plot .plotly .bg {
        fill: transparent !important;
    }

    /* ── Opportunity table ── */
    .opp-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.88rem;
    }
    .opp-theme { flex: 2; color: #f1f5f9; font-weight: 500; }
    .opp-coverage { flex: 1; color: #94a3b8; text-align: center; }
    .opp-score { flex: 1; text-align: center; }
    .opp-rec { flex: 3; color: #94a3b8; font-size: 0.82rem; }
    .score-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .score-high { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
    .score-mid { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
    .score-low { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
    </style>
    """, unsafe_allow_html=True)


# ─── Plotly Theme ─────────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Grotesk", color="#94a3b8", size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
        font=dict(size=11)
    ),
)

def _apply_axis_style(fig):
    """Apply consistent axis styling without conflicting with update_layout kwargs."""
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.1)")
    return fig

COLORS = ["#8b5cf6", "#ec4899", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"]


def fmt_num(n: float) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(int(n))


# ─── Header ──────────────────────────────────────────────────────────────────

def render_header():
    st.markdown("""
    <div class="war-room-header">
        <div class="header-eyebrow">🛰️ Competitive Intelligence Platform</div>
        <h1 class="header-title">AI Video Marketing War Room</h1>
        <p class="header-subtitle">YouTube competitive intelligence, content gap detection, and AI-powered strategic recommendations.</p>
        <br/>
        <span class="header-badge">Real-time Analysis</span>
        <span class="header-badge">AI-Powered</span>
        <span class="header-badge">10-Tab Intelligence</span>
        <span class="header-badge">PPT Export</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Input Section ────────────────────────────────────────────────────────────

def render_input_section():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🎯 Intelligence Target Setup</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Enter your brand and up to 4 competitor names to begin the analysis.</div>', unsafe_allow_html=True)

    col_main, col_c1, col_c2 = st.columns([2, 1, 1])
    with col_main:
        user_company = st.text_input("🏢 Your Company", placeholder="e.g. HubSpot", key="user_co")
    with col_c1:
        c1 = st.text_input("Competitor 1", placeholder="e.g. Salesforce", key="c1")
    with col_c2:
        c2 = st.text_input("Competitor 2", placeholder="e.g. Mailchimp", key="c2")

    col_c3, col_c4, _ = st.columns([1, 1, 2])
    with col_c3:
        c3 = st.text_input("Competitor 3", placeholder="e.g. ActiveCampaign", key="c3")
    with col_c4:
        c4 = st.text_input("Competitor 4 (optional)", placeholder="e.g. Klaviyo", key="c4")

    st.markdown('</div>', unsafe_allow_html=True)
    return user_company, [c1, c2, c3, c4]


# ─── Tab 1: Executive Summary ─────────────────────────────────────────────────

def render_executive_summary(analytics: AnalyticsEngine, channel_data: dict, user_company: str):
    es = analytics.executive_summary
    metrics = analytics.metrics

    st.markdown('<div class="section-title">📊 Executive Intelligence Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">High-level competitive landscape analysis and strategic positioning.</div>', unsafe_allow_html=True)

    # ── Top KPIs ──
    cols = st.columns(4)
    user_m = metrics.get(user_company, {})
    with cols[0]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Your Threat Score</div>
            <div class="kpi-value">{es.get('user_threat_score', 0)}<span style="font-size:1rem;color:#64748b">/10</span></div>
            <div class="kpi-sub">Overall competitive power</div>
        </div>""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Top Rival</div>
            <div class="kpi-value" style="font-size:1.2rem;">{es.get('strongest_rival','N/A')}</div>
            <div class="kpi-sub">Score: {es.get('strongest_rival_score', 0)}/10</div>
        </div>""", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Top Opportunity</div>
            <div class="kpi-value" style="font-size:1.2rem;">{es.get('top_opportunity','N/A')}</div>
            <div class="kpi-sub">White space content theme</div>
        </div>""", unsafe_allow_html=True)
    with cols[3]:
        gap = es.get('sub_gap', 0)
        gap_class = "kpi-down" if gap > 0 else "kpi-up"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Subscriber Gap</div>
            <div class="kpi-value {gap_class}">{fmt_num(abs(gap))}</div>
            <div class="kpi-sub">{'Behind avg competitor' if gap > 0 else 'Ahead of avg competitor'}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Strategic Insights ──
    col_left, col_right = st.columns([3, 2])
    with col_left:
        st.markdown("**🧠 Strategic Intelligence Findings**")
        st.markdown(f'<div class="insight-box red">⚠️ {es.get("insight_1", "")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-box green">🟢 {es.get("insight_2", "")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-box yellow">🎯 {es.get("insight_3", "")}</div>', unsafe_allow_html=True)

    with col_right:
        # Mini subscriber bar chart
        companies = list(metrics.keys())
        subs = [metrics[c]["subscribers"] for c in companies]
        fig = go.Figure(go.Bar(
            x=companies,
            y=subs,
            marker=dict(
                color=subs,
                colorscale=[[0, "#4c1d95"], [1, "#a78bfa"]],
                showscale=False
            ),
            text=[fmt_num(s) for s in subs],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=11)
        ))
        layout = {**PLOTLY_LAYOUT, "title": "Subscriber Comparison", "height": 280}
        layout["yaxis"] = dict(showticklabels=False, gridcolor="rgba(255,255,255,0.04)")
        fig.update_layout(**layout)
        _apply_axis_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    # ── Competitive Ranking Table ──
    st.markdown("<br/>**📋 Competitive Intelligence Matrix**")
    table_data = []
    for c in list(metrics.keys()):
        m = metrics[c]
        aei = analytics.aei_scores.get(c, 0)
        threat = analytics.threat_scores.get(c, {}).get("total", 0)
        table_data.append({
            "Company": "⭐ " + c if c == user_company else c,
            "Subscribers": fmt_num(m["subscribers"]),
            "Avg Views": fmt_num(m["avg_views"]),
            "Engagement %": f"{m['engagement_rate']:.2f}%",
            "AEI Score": f"{aei:.1f}%",
            "Uploads/Mo": str(m["upload_freq"]),
            "Threat Score": f"{threat}/10",
        })
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ─── Tab 2: Channel Intelligence ─────────────────────────────────────────────

def render_channel_intelligence(analytics: AnalyticsEngine, channel_data: dict):
    metrics = analytics.metrics
    companies = list(metrics.keys())

    st.markdown('<div class="section-title">📡 Channel Intelligence</div>', unsafe_allow_html=True)

    # ── KPI Cards Row ──
    cols = st.columns(len(companies))
    for i, c in enumerate(companies):
        m = metrics[c]
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{c}</div>
                <div class="kpi-value">{fmt_num(m['subscribers'])}</div>
                <div class="kpi-sub">{fmt_num(m['total_videos'])} videos · {fmt_num(m['total_views'])} total views</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Grouped Bar Chart ──
    col_l, col_r = st.columns(2)
    with col_l:
        fig = go.Figure()
        metrics_to_show = [("Subscribers", "subscribers"), ("Total Videos (×10)", "total_videos")]
        for j, (label, key) in enumerate(metrics_to_show):
            vals = [metrics[c][key] / (10 if key == "total_videos" else 1) for c in companies]
            fig.add_trace(go.Bar(
                name=label, x=companies, y=vals,
                marker_color=COLORS[j],
                text=[fmt_num(metrics[c][key]) for c in companies],
                textposition="outside",
                textfont=dict(size=10)
            ))
        fig.update_layout(**PLOTLY_LAYOUT, barmode="group", title="Channel Size Metrics", height=350)
        _apply_axis_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Upload frequency comparison
        freqs = [metrics[c]["upload_freq"] for c in companies]
        fig2 = go.Figure(go.Bar(
            x=companies, y=freqs,
            marker=dict(color=COLORS[2]),
            text=[f"{f} /mo" for f in freqs],
            textposition="outside"
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, title="Upload Frequency (videos/month)", height=350)
        _apply_axis_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Total Views Trend (simulated from top videos) ──
    st.markdown("**📈 Top Video Performance by Company**")
    fig3 = go.Figure()
    for i, c in enumerate(companies):
        top_vids = channel_data[c].get("top_videos", [])[:10]
        titles = [v["title"][:30] + "..." for v in top_vids]
        views = [v["views"] for v in top_vids]
        fig3.add_trace(go.Scatter(
            x=list(range(1, len(views) + 1)),
            y=views,
            name=c,
            mode="lines+markers",
            line=dict(color=COLORS[i], width=2),
            marker=dict(size=7),
            hovertemplate="%{text}<br>Views: %{y:,}",
            text=titles
        ))
    fig3.update_layout(**PLOTLY_LAYOUT, title="Top 10 Videos — Views Comparison", height=360,
                       xaxis_title="Video Rank", yaxis_title="Views")
    _apply_axis_style(fig3)
    st.plotly_chart(fig3, use_container_width=True)


# ─── Tab 3: Engagement Intelligence ──────────────────────────────────────────

def render_engagement_intelligence(analytics: AnalyticsEngine, channel_data: dict):
    metrics = analytics.metrics
    companies = list(metrics.keys())

    st.markdown('<div class="section-title">💥 Engagement Intelligence</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        # Radar chart
        categories = ["Avg Views", "Avg Likes", "Avg Comments", "Engagement Rate", "Upload Freq"]
        fig = go.Figure()

        def normalize_list(vals):
            max_v = max(vals) if max(vals) > 0 else 1
            return [v / max_v * 10 for v in vals]

        raw_data = {
            "Avg Views": [metrics[c]["avg_views"] for c in companies],
            "Avg Likes": [metrics[c]["avg_likes"] for c in companies],
            "Avg Comments": [metrics[c]["avg_comments"] for c in companies],
            "Engagement Rate": [metrics[c]["engagement_rate"] for c in companies],
            "Upload Freq": [metrics[c]["upload_freq"] for c in companies],
        }

        for i, c in enumerate(companies):
            r_vals = [normalize_list(raw_data[cat])[i] for cat in categories]
            r_vals.append(r_vals[0])
            fig.add_trace(go.Scatterpolar(
                r=r_vals,
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor=f"rgba({','.join(str(x) for x in _hex_to_rgb(COLORS[i]))}, 0.1)",
                line=dict(color=COLORS[i], width=2),
                name=c
            ))
        fig.update_layout(
            **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis", "yaxis"]},
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9)),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.08)")
            ),
            title="Engagement Radar",
            height=420
        )
        _apply_axis_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Engagement rate bars
        eng_rates = [metrics[c]["engagement_rate"] for c in companies]
        fig2 = go.Figure(go.Bar(
            x=companies,
            y=eng_rates,
            marker=dict(
                color=eng_rates,
                colorscale=[[0, "#4c1d95"], [0.5, "#8b5cf6"], [1, "#34d399"]],
            ),
            text=[f"{e:.2f}%" for e in eng_rates],
            textposition="outside"
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, title="Engagement Rate (%)", height=200)
        _apply_axis_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        # Avg views / likes comparison
        fig3 = make_subplots(rows=1, cols=2, subplot_titles=["Avg Views", "Avg Likes"])
        fig3.add_trace(go.Bar(x=companies, y=[metrics[c]["avg_views"] for c in companies],
                              marker_color=COLORS[0], showlegend=False), row=1, col=1)
        fig3.add_trace(go.Bar(x=companies, y=[metrics[c]["avg_likes"] for c in companies],
                              marker_color=COLORS[1], showlegend=False), row=1, col=2)
        fig3.update_layout(**PLOTLY_LAYOUT, height=200)
        _apply_axis_style(fig3)
        st.plotly_chart(fig3, use_container_width=True)


# ─── Tab 4: AEI Index ─────────────────────────────────────────────────────────

def render_aei_analysis(analytics: AnalyticsEngine, channel_data: dict):
    aei = analytics.aei_scores
    companies = sorted(aei.keys(), key=lambda c: aei[c], reverse=True)

    st.markdown('<div class="section-title">🎯 Attention Efficiency Index (AEI)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
        <strong>What is AEI?</strong> The Attention Efficiency Index = (Average Views per Video / Subscribers) × 100.
        A score above 30% indicates highly activated audiences. Below 10% may signal subscriber decay or inactive followers.
    </div>""", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])
    with col_l:
        fig = go.Figure(go.Bar(
            x=[aei[c] for c in companies],
            y=companies,
            orientation="h",
            marker=dict(
                color=[aei[c] for c in companies],
                colorscale=[[0, "#7c3aed"], [0.5, "#ec4899"], [1, "#34d399"]],
            ),
            text=[f"{aei[c]:.1f}%" for c in companies],
            textposition="outside"
        ))
        fig.update_layout(**PLOTLY_LAYOUT, title="AEI Leaderboard", height=350,
                          xaxis_title="AEI Score (%)")
        _apply_axis_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown("**📊 AEI Scorecards**")
        for c in companies:
            score = aei[c]
            tier = "🟢 Excellent" if score > 30 else "🟡 Average" if score > 10 else "🔴 Needs Work"
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left; margin-bottom:0.6rem; padding:1rem">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div class="kpi-label" style="margin:0">{c}</div>
                    <div>{tier}</div>
                </div>
                <div class="kpi-value" style="font-size:1.5rem">{score:.1f}%</div>
                <div class="threat-bar"><div class="threat-bar-fill" style="width:{min(score*2, 100):.0f}%"></div></div>
            </div>""", unsafe_allow_html=True)


# ─── Tab 5: Content Themes ────────────────────────────────────────────────────

def render_content_themes(analytics: AnalyticsEngine, channel_data: dict):
    themes = analytics.content_themes
    companies = list(themes.keys())
    all_theme_keys = list(set(k for t in themes.values() for k in t.keys()))

    st.markdown('<div class="section-title">🎨 Content Theme Intelligence</div>', unsafe_allow_html=True)

    fig = go.Figure()
    for i, theme in enumerate(all_theme_keys):
        vals = [themes[c].get(theme, 0) for c in companies]
        fig.add_trace(go.Bar(
            name=theme, x=companies, y=vals,
            marker_color=COLORS[i % len(COLORS)]
        ))
    fig.update_layout(**PLOTLY_LAYOUT, barmode="stack", title="Content Theme Distribution", height=400)
    _apply_axis_style(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Pie charts per company
    cols = st.columns(min(len(companies), 4))
    for i, c in enumerate(companies[:4]):
        with cols[i]:
            t_data = themes.get(c, {})
            if t_data:
                fig_pie = go.Figure(go.Pie(
                    labels=list(t_data.keys()),
                    values=list(t_data.values()),
                    hole=0.5,
                    marker=dict(colors=COLORS[:len(t_data)]),
                    textfont=dict(size=10),
                    showlegend=True
                ))
                pie_layout = {k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis", "yaxis", "legend"]}
                pie_layout["title"] = c
                pie_layout["height"] = 280
                pie_layout["legend"] = dict(font=dict(size=9), orientation="v")
                fig_pie.update_layout(**pie_layout)
                _apply_axis_style(fig_pie)
                st.plotly_chart(fig_pie, use_container_width=True)


# ─── Tab 6: Viral Patterns ────────────────────────────────────────────────────

def render_viral_patterns(analytics: AnalyticsEngine, channel_data: dict):
    viral = analytics.viral_insights
    companies = list(viral.keys())

    st.markdown('<div class="section-title">🔥 Viral Pattern Analysis</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        # Emotional vs Promo comparison
        emo_vals = [viral[c].get("emotional_avg_views", 0) for c in companies]
        promo_vals = [viral[c].get("promo_avg_views", 0) for c in companies]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Emotional / Story", x=companies, y=emo_vals,
                             marker_color=COLORS[0]))
        fig.add_trace(go.Bar(name="Promotional", x=companies, y=promo_vals,
                             marker_color=COLORS[1]))
        fig.update_layout(**PLOTLY_LAYOUT, barmode="group", title="Emotional vs Promotional Views", height=320)
        _apply_axis_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Title length performance
        short_vals = [viral[c].get("short_title_avg", 0) for c in companies]
        long_vals = [viral[c].get("long_title_avg", 0) for c in companies]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Short Titles (<40 chars)", x=companies, y=short_vals,
                              marker_color=COLORS[2]))
        fig2.add_trace(go.Bar(name="Long Titles (≥40 chars)", x=companies, y=long_vals,
                              marker_color=COLORS[3]))
        fig2.update_layout(**PLOTLY_LAYOUT, barmode="group", title="Title Length vs Performance", height=320)
        _apply_axis_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # Best posting day insight
    st.markdown("**📅 Optimal Posting Intelligence**")
    day_cols = st.columns(len(companies))
    for i, c in enumerate(companies):
        v = viral.get(c, {})
        ratio = v.get("emotional_vs_promo_ratio", 1)
        best_day = v.get("best_day", "Tuesday")
        with day_cols[i]:
            st.markdown(f"""
            <div class="glass-card-accent">
                <div class="kpi-label">{c}</div>
                <div style="font-size:0.9rem; color:#f1f5f9; margin:0.5rem 0">
                    🗓️ Best day: <strong>{best_day}</strong>
                </div>
                <div class="insight-box" style="margin:0; font-size:0.82rem">
                    Emotional content outperforms promotional by <strong>{ratio:.1f}x</strong>
                </div>
            </div>""", unsafe_allow_html=True)


# ─── Tab 7: White Space Map ───────────────────────────────────────────────────

def render_whitespace_map(analytics: AnalyticsEngine, channel_data: dict, user_company: str):
    whitespace = analytics.whitespace

    st.markdown('<div class="section-title">🗺️ White Space Opportunity Map</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box green">
        Strategic content gaps detected by comparing competitor coverage against content category availability.
        High opportunity scores indicate low competition and high potential for organic growth.
    </div>""", unsafe_allow_html=True)

    # Table header
    st.markdown("""
    <div style="display:flex;gap:1rem;padding:0.5rem 1rem;border-bottom:2px solid rgba(255,255,255,0.1);font-size:0.75rem;color:#64748b;font-weight:600;letter-spacing:0.1em;text-transform:uppercase">
        <div style="flex:2">Content Theme</div>
        <div style="flex:1;text-align:center">Competitor Coverage</div>
        <div style="flex:1;text-align:center">Opportunity Score</div>
        <div style="flex:1;text-align:center">You Have It?</div>
        <div style="flex:3">Recommendation</div>
    </div>""", unsafe_allow_html=True)

    for row in whitespace:
        score = row["opportunity_score"]
        badge_class = "score-high" if score >= 7 else "score-mid" if score >= 4 else "score-low"
        has_it = "✅ Yes" if row["you_have_it"] else "❌ No"
        st.markdown(f"""
        <div class="opp-row">
            <div class="opp-theme">📌 {row['theme']}</div>
            <div class="opp-coverage">{row['competitor_coverage']}</div>
            <div class="opp-score"><span class="score-badge {badge_class}">{score}/10</span></div>
            <div class="opp-coverage">{has_it}</div>
            <div class="opp-rec">{row['recommendation']}</div>
        </div>""", unsafe_allow_html=True)

    # Opportunity heatmap
    st.markdown("<br/>**📊 Opportunity Score Heatmap**")
    themes = [r["theme"] for r in whitespace]
    scores = [r["opportunity_score"] for r in whitespace]
    fig = go.Figure(go.Bar(
        x=themes,
        y=scores,
        marker=dict(
            color=scores,
            colorscale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#10b981"]],
            cmin=0, cmax=10
        ),
        text=[f"{s}/10" for s in scores],
        textposition="outside"
    ))
    fig.update_layout(**PLOTLY_LAYOUT, title="White Space Opportunity Scores", height=320, yaxis_range=[0, 12])
    _apply_axis_style(fig)
    st.plotly_chart(fig, use_container_width=True)


# ─── Tab 8: Threat Scoring ────────────────────────────────────────────────────

def render_threat_scoring(analytics: AnalyticsEngine, channel_data: dict):
    threat = analytics.threat_scores
    companies = sorted(threat.keys(), key=lambda c: threat[c]["total"], reverse=True)
    dimensions = ["Engagement Power", "Audience Loyalty", "Posting Consistency",
                  "SEO Optimization", "Content Diversity", "Growth Potential"]

    st.markdown('<div class="section-title">⚠️ Competitive Threat Scoring</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([2, 3])
    with col_l:
        st.markdown("**🏆 Threat Score Leaderboard**")
        for rank, c in enumerate(companies):
            total = threat[c]["total"]
            medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][rank] if rank < 5 else str(rank + 1)
            width_pct = int(total * 10)
            st.markdown(f"""
            <div style="padding:0.75rem 0; border-bottom:1px solid rgba(255,255,255,0.05)">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="color:#f1f5f9;font-weight:500">{medal} {c}</span>
                    <span style="color:#a78bfa;font-weight:700">{total}/10</span>
                </div>
                <div class="threat-bar"><div class="threat-bar-fill" style="width:{width_pct}%"></div></div>
            </div>""", unsafe_allow_html=True)

    with col_r:
        # Radar per company
        fig = go.Figure()
        for i, c in enumerate(companies):
            scores = [threat[c].get(d, 0) for d in dimensions]
            scores.append(scores[0])
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=dimensions + [dimensions[0]],
                fill="toself",
                fillcolor=f"rgba({','.join(str(x) for x in _hex_to_rgb(COLORS[i]))}, 0.08)",
                line=dict(color=COLORS[i], width=2),
                name=c
            ))
        fig.update_layout(
            **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["xaxis", "yaxis"]},
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9)),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.08)")
            ),
            title="Competitive Threat Matrix",
            height=420
        )
        _apply_axis_style(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Score breakdown table
    st.markdown("**📋 Score Breakdown**")
    rows = []
    for c in companies:
        row = {"Company": c}
        for d in dimensions:
            row[d] = f"{threat[c].get(d, 0):.1f}"
        row["TOTAL"] = f"{threat[c]['total']:.1f}"
        rows.append(row)
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


# ─── Tab 9: AI Recommendations ────────────────────────────────────────────────

def render_ai_recommendations(analytics: AnalyticsEngine, user_company: str):
    recs = analytics.recommendations

    st.markdown('<div class="section-title">🤖 AI Strategic Recommendations</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">Personalized strategy for <strong>{user_company}</strong> based on competitive intelligence analysis.</div>', unsafe_allow_html=True)

    icons = {
        "content_strategy": ("🎯", "Content Strategy"),
        "upload_cadence": ("📅", "Upload Cadence"),
        "shorts_strategy": ("⚡", "Shorts Strategy"),
        "engagement_tips": ("💬", "Engagement Improvement"),
        "differentiation": ("🚀", "Differentiation Blueprint"),
    }

    for key, (icon, title) in icons.items():
        text = recs.get(key, "No recommendation available.")
        st.markdown(f"""
        <div class="glass-card-accent" style="margin-bottom:1rem">
            <div style="font-size:0.85rem;font-weight:700;color:#a78bfa;margin-bottom:0.5rem">{icon} {title}</div>
            <div style="color:#cbd5e1;font-size:0.92rem;line-height:1.7">{text}</div>
        </div>""", unsafe_allow_html=True)


# ─── Tab 10: Content Roadmap ──────────────────────────────────────────────────

def render_content_roadmap(analytics: AnalyticsEngine, user_company: str):
    roadmap = analytics.roadmap

    st.markdown('<div class="section-title">📅 30-Day Content Roadmap</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-subtitle">Week-by-week execution plan for <strong>{user_company}</strong>.</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, (week, data) in enumerate(roadmap.items()):
        with cols[i % 2]:
            actions_html = "".join(
                f'<div class="roadmap-action">→ {a}</div>' for a in data["actions"]
            )
            st.markdown(f"""
            <div class="roadmap-week">
                <div class="roadmap-week-title">{week}: {data['title']}</div>
                {actions_html}
                <div class="roadmap-goal">🎯 Goal: {data['goal']}</div>
            </div>""", unsafe_allow_html=True)


# ─── Utilities ────────────────────────────────────────────────────────────────

def _hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
