"""
ppt_generator.py — Premium PowerPoint intelligence report generator.
Dark theme, consulting-quality layouts, charts embedded as images.
"""

import io
import statistics
from datetime import datetime

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import pptx.util as pptx_util

# ─── Color Palette ────────────────────────────────────────────────────────────
BG_DARK      = RGBColor(0x08, 0x0C, 0x14)
BG_CARD      = RGBColor(0x0F, 0x17, 0x2A)
ACCENT_PURPLE = RGBColor(0x8B, 0x5C, 0xF6)
ACCENT_PINK  = RGBColor(0xEC, 0x48, 0x99)
ACCENT_CYAN  = RGBColor(0x06, 0xB6, 0xD4)
ACCENT_GREEN = RGBColor(0x10, 0xB9, 0x81)
ACCENT_AMBER = RGBColor(0xF5, 0x9E, 0x0B)
TEXT_PRIMARY = RGBColor(0xF1, 0xF5, 0xF9)
TEXT_MUTED   = RGBColor(0x94, 0xA3, 0xB8)
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)


def fmt_num(n: float) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(int(n))


# ─── Slide Builder Helpers ────────────────────────────────────────────────────

def _set_bg(slide, prs):
    """Fill slide background with dark color."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG_DARK


def _add_text(slide, text, left, top, width, height,
              font_size=14, bold=False, color=TEXT_PRIMARY,
              align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def _add_rect(slide, left, top, width, height, fill_color, alpha=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    return shape


def _add_slide(prs):
    layout = prs.slide_layouts[6]  # blank
    slide = prs.slides.add_slide(layout)
    _set_bg(slide, prs)
    return slide


def _add_header_bar(slide, prs, title: str, subtitle: str = ""):
    W = prs.slide_width
    # Purple top accent line
    _add_rect(slide, 0, 0, W, Pt(4), ACCENT_PURPLE)
    # Title
    _add_text(slide, title, Inches(0.5), Inches(0.18), W - Inches(1), Inches(0.6),
              font_size=24, bold=True, color=TEXT_PRIMARY)
    if subtitle:
        _add_text(slide, subtitle, Inches(0.5), Inches(0.72), W - Inches(1), Inches(0.35),
                  font_size=11, color=TEXT_MUTED)


def _add_kpi_box(slide, label, value, sub, left, top, w=Inches(2), h=Inches(1.1),
                 accent=ACCENT_PURPLE):
    _add_rect(slide, left, top, w, h, BG_CARD)
    # Accent left border
    _add_rect(slide, left, top, Inches(0.04), h, accent)
    _add_text(slide, label, left + Inches(0.12), top + Inches(0.08), w - Inches(0.2), Inches(0.22),
              font_size=8, color=TEXT_MUTED, bold=True)
    _add_text(slide, value, left + Inches(0.12), top + Inches(0.28), w - Inches(0.2), Inches(0.5),
              font_size=20, bold=True, color=TEXT_PRIMARY)
    _add_text(slide, sub, left + Inches(0.12), top + Inches(0.78), w - Inches(0.2), Inches(0.25),
              font_size=8, color=TEXT_MUTED)


def _add_insight_box(slide, text, left, top, width, height, accent=ACCENT_PURPLE):
    _add_rect(slide, left, top, width, height, RGBColor(0x10, 0x18, 0x2A))
    _add_rect(slide, left, top, Inches(0.04), height, accent)
    _add_text(slide, text, left + Inches(0.12), top + Inches(0.1), width - Inches(0.2), height - Inches(0.15),
              font_size=10, color=TEXT_PRIMARY, italic=False)


def _add_bar_chart_manual(slide, companies, values, title, left, top, width, height,
                           color=ACCENT_PURPLE, show_values=True):
    """Draw a simple horizontal bar chart using rectangles."""
    _add_text(slide, title, left, top, width, Inches(0.3),
              font_size=11, bold=True, color=TEXT_MUTED)
    top += Inches(0.35)
    height -= Inches(0.35)

    if not values or max(values) == 0:
        return

    bar_h = height / max(len(companies), 1)
    max_val = max(values)

    for i, (company, val) in enumerate(zip(companies, values)):
        bar_y = top + i * bar_h + bar_h * 0.1
        bar_actual_h = bar_h * 0.7
        bar_w = (val / max_val) * (width - Inches(1.4))

        # Label
        _add_text(slide, company[:15], left, bar_y, Inches(1.2), bar_actual_h,
                  font_size=9, color=TEXT_MUTED)

        # Bar
        _add_rect(slide, left + Inches(1.3), bar_y, bar_w, bar_actual_h, color)

        # Value
        if show_values:
            val_str = fmt_num(val) if isinstance(val, (int, float)) else str(val)
            _add_text(slide, val_str,
                      left + Inches(1.3) + bar_w + Inches(0.05), bar_y, Inches(0.8), bar_actual_h,
                      font_size=9, color=TEXT_PRIMARY, bold=True)


# ─── Main PPT Generator ───────────────────────────────────────────────────────

def generate_ppt_report(analytics, channel_data: dict, user_company: str) -> bytes:
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    W = prs.slide_width
    H = prs.slide_height

    metrics = analytics.metrics
    companies = list(metrics.keys())
    threat = analytics.threat_scores
    aei = analytics.aei_scores
    es = analytics.executive_summary
    whitespace = analytics.whitespace
    recs = analytics.recommendations
    roadmap = analytics.roadmap
    viral = analytics.viral_insights
    themes = analytics.content_themes

    # ── SLIDE 1: Title ──────────────────────────────────────────────────────
    slide = _add_slide(prs)
    # Gradient-style overlay rect
    _add_rect(slide, 0, 0, W, H, RGBColor(0x0F, 0x0A, 0x1F))
    _add_rect(slide, 0, 0, Inches(0.1), H, ACCENT_PURPLE)

    _add_text(slide, "AI VIDEO MARKETING", Inches(0.8), Inches(1.5), W - Inches(1.5), Inches(1),
              font_size=40, bold=True, color=TEXT_PRIMARY)
    _add_text(slide, "WAR ROOM", Inches(0.8), Inches(2.5), W - Inches(1.5), Inches(0.9),
              font_size=52, bold=True, color=ACCENT_PURPLE)
    _add_text(slide, "Competitive Intelligence Report", Inches(0.8), Inches(3.5), W - Inches(1.5), Inches(0.5),
              font_size=18, color=TEXT_MUTED)
    _add_text(slide, f"Subject: {user_company} vs {', '.join(c for c in companies if c != user_company)}",
              Inches(0.8), Inches(4.1), W - Inches(1.5), Inches(0.4),
              font_size=13, color=ACCENT_CYAN)
    _add_text(slide, f"Generated: {datetime.now().strftime('%B %d, %Y')}",
              Inches(0.8), Inches(4.55), W - Inches(1.5), Inches(0.3),
              font_size=10, color=TEXT_MUTED)
    _add_rect(slide, Inches(0.8), Inches(5.1), Inches(4), Inches(0.05), ACCENT_PINK)
    _add_text(slide, "CONFIDENTIAL · STRATEGIC INTELLIGENCE", Inches(0.8), Inches(5.2), W, Inches(0.3),
              font_size=9, color=RGBColor(0x4C, 0x1D, 0x95), bold=True)

    # ── SLIDE 2: Executive Summary ──────────────────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Executive Summary", "High-level competitive landscape findings")

    user_m = metrics.get(user_company, {})
    _add_kpi_box(slide, "THREAT SCORE", f"{es.get('user_threat_score', 0)}/10",
                 user_company, Inches(0.4), Inches(1.2), Inches(2.1), accent=ACCENT_PURPLE)
    _add_kpi_box(slide, "TOP RIVAL", es.get('strongest_rival', 'N/A'),
                 f"Score: {es.get('strongest_rival_score', 0)}/10", Inches(2.7), Inches(1.2), Inches(2.1), accent=ACCENT_PINK)
    _add_kpi_box(slide, "TOP OPPORTUNITY", es.get('top_opportunity', 'N/A'),
                 "Content white space", Inches(5.0), Inches(1.2), Inches(2.1), accent=ACCENT_CYAN)
    _add_kpi_box(slide, "YOUR SUBSCRIBERS", fmt_num(user_m.get('subscribers', 0)),
                 "vs competitors", Inches(7.3), Inches(1.2), Inches(2.1), accent=ACCENT_GREEN)
    _add_kpi_box(slide, "ENGAGEMENT RATE", f"{user_m.get('engagement_rate', 0):.2f}%",
                 "avg across videos", Inches(9.6), Inches(1.2), Inches(2.1), accent=ACCENT_AMBER)

    _add_text(slide, "KEY STRATEGIC FINDINGS", Inches(0.4), Inches(2.55), W - Inches(0.8), Inches(0.3),
              font_size=9, bold=True, color=TEXT_MUTED)
    _add_insight_box(slide, f"⚠ {es.get('insight_1', '')}", Inches(0.4), Inches(2.9), W - Inches(0.8), Inches(0.75), ACCENT_PINK)
    _add_insight_box(slide, f"✓ {es.get('insight_2', '')}", Inches(0.4), Inches(3.75), W - Inches(0.8), Inches(0.75), ACCENT_GREEN)
    _add_insight_box(slide, f"→ {es.get('insight_3', '')}", Inches(0.4), Inches(4.6), W - Inches(0.8), Inches(0.75), ACCENT_AMBER)

    # ── SLIDE 3: Channel Intelligence ───────────────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Channel Intelligence", "Subscribers, videos, total views comparison")

    subs = [metrics[c]["subscribers"] for c in companies]
    _add_bar_chart_manual(slide, companies, subs, "Subscriber Count",
                          Inches(0.4), Inches(1.1), Inches(5.5), Inches(2.8), ACCENT_PURPLE)

    total_vids = [metrics[c]["total_videos"] for c in companies]
    _add_bar_chart_manual(slide, companies, total_vids, "Total Videos Published",
                          Inches(6.8), Inches(1.1), Inches(5.5), Inches(2.8), ACCENT_CYAN)

    upload_freqs = [metrics[c]["upload_freq"] for c in companies]
    _add_bar_chart_manual(slide, companies, upload_freqs, "Upload Frequency (videos/month)",
                          Inches(0.4), Inches(4.1), Inches(5.5), Inches(2.8), ACCENT_PINK)

    total_views = [metrics[c]["total_views"] for c in companies]
    _add_bar_chart_manual(slide, companies, total_views, "Total Channel Views",
                          Inches(6.8), Inches(4.1), Inches(5.5), Inches(2.8), ACCENT_GREEN)

    # ── SLIDE 4: Engagement Intelligence ────────────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Engagement Intelligence", "Avg views, likes, comments, and engagement rate")

    col_x = [Inches(0.4), Inches(3.1), Inches(5.8), Inches(8.5), Inches(11.2)]
    top_y = Inches(1.2)
    box_w = Inches(2.4)
    for i, c in enumerate(companies[:5]):
        m = metrics[c]
        _add_kpi_box(slide, c.upper()[:12], fmt_num(m["avg_views"]),
                     f"Avg Views · {m['engagement_rate']:.1f}% Eng",
                     col_x[i], top_y, box_w,
                     accent=COLORS_RGB[i % len(COLORS_RGB)])

    avg_views = [metrics[c]["avg_views"] for c in companies]
    _add_bar_chart_manual(slide, companies, avg_views, "Average Views per Video",
                          Inches(0.4), Inches(2.55), Inches(5.8), Inches(3.5), ACCENT_PURPLE)

    eng_rates = [metrics[c]["engagement_rate"] for c in companies]
    _add_bar_chart_manual(slide, companies, eng_rates, "Engagement Rate (%)",
                          Inches(7.0), Inches(2.55), Inches(5.8), Inches(3.5), ACCENT_CYAN)

    # ── SLIDE 5: AEI Index ────────────────────────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Attention Efficiency Index (AEI)", "AEI = Avg Views / Subscribers × 100%")

    _add_insight_box(slide,
                     "AEI measures how efficiently a brand converts its subscriber base into actual viewers. "
                     "Scores above 30% indicate highly activated audiences with strong content-channel fit.",
                     Inches(0.4), Inches(1.15), W - Inches(0.8), Inches(0.7), ACCENT_PURPLE)

    aei_sorted = sorted(aei.items(), key=lambda x: x[1], reverse=True)
    companies_sorted = [x[0] for x in aei_sorted]
    aei_vals = [x[1] for x in aei_sorted]

    _add_bar_chart_manual(slide, companies_sorted, aei_vals, "AEI Leaderboard (%)",
                          Inches(0.4), Inches(2.1), W - Inches(0.8), Inches(4.5), ACCENT_PURPLE)

    # ── SLIDE 6: Content Theme Intelligence ──────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Content Theme Intelligence", "Video topic distribution across competitors")

    row_y = Inches(1.15)
    for i, (company, theme_data) in enumerate(list(themes.items())[:5]):
        col_x = Inches(0.4) + i * Inches(2.5)
        _add_text(slide, company[:14], col_x, row_y, Inches(2.4), Inches(0.3),
                  font_size=10, bold=True, color=ACCENT_PURPLE)
        bar_top = row_y + Inches(0.35)
        total_vids = sum(theme_data.values()) or 1

        for j, (theme, count) in enumerate(sorted(theme_data.items(), key=lambda x: x[1], reverse=True)[:6]):
            pct = count / total_vids
            bar_w = pct * Inches(2.2)
            _add_text(slide, theme[:14], col_x, bar_top + j * Inches(0.85), Inches(2.4), Inches(0.25),
                      font_size=8, color=TEXT_MUTED)
            _add_rect(slide, col_x, bar_top + j * Inches(0.85) + Inches(0.28), bar_w, Inches(0.28),
                      COLORS_RGB[j % len(COLORS_RGB)])
            _add_text(slide, f"{int(pct*100)}%",
                      col_x + bar_w + Inches(0.05), bar_top + j * Inches(0.85) + Inches(0.28),
                      Inches(0.4), Inches(0.28), font_size=8, color=TEXT_PRIMARY)

    # ── SLIDE 7: White Space Opportunity Map ─────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "White Space Opportunity Map", "Content gaps and untapped strategic opportunities")

    cols_header = ["Theme", "Coverage", "Opp Score", "Recommendation"]
    col_widths = [Inches(1.8), Inches(1.0), Inches(1.0), Inches(8.0)]
    col_x_positions = [Inches(0.4), Inches(2.3), Inches(3.4), Inches(4.5)]
    row_h = Inches(0.42)
    header_y = Inches(1.15)

    for j, (header, cx) in enumerate(zip(cols_header, col_x_positions)):
        _add_text(slide, header, cx, header_y, col_widths[j], Inches(0.28),
                  font_size=8, bold=True, color=ACCENT_PURPLE)

    for i, row in enumerate(whitespace[:11]):
        row_y = header_y + Inches(0.32) + i * row_h
        bg_color = RGBColor(0x0F, 0x17, 0x2A) if i % 2 == 0 else BG_DARK
        _add_rect(slide, Inches(0.35), row_y, W - Inches(0.7), row_h - Inches(0.04), bg_color)

        score = row["opportunity_score"]
        score_color = ACCENT_GREEN if score >= 7 else ACCENT_AMBER if score >= 4 else RGBColor(0xEF, 0x44, 0x44)

        _add_text(slide, row["theme"], col_x_positions[0], row_y + Inches(0.06),
                  col_widths[0], row_h, font_size=9, color=TEXT_PRIMARY)
        _add_text(slide, row["competitor_coverage"], col_x_positions[1], row_y + Inches(0.06),
                  col_widths[1], row_h, font_size=9, color=TEXT_MUTED)
        _add_text(slide, f"{score}/10", col_x_positions[2], row_y + Inches(0.06),
                  col_widths[2], row_h, font_size=10, bold=True, color=score_color)
        _add_text(slide, row["recommendation"][:80], col_x_positions[3], row_y + Inches(0.04),
                  col_widths[3], row_h, font_size=8, color=TEXT_MUTED)

    # ── SLIDE 8: Competitive Threat Scoring ──────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Competitive Threat Scoring", "Multi-dimensional brand power analysis")

    dimensions = ["Engagement Power", "Audience Loyalty", "Posting Consistency",
                  "SEO Optimization", "Content Diversity", "Growth Potential"]

    sorted_companies = sorted(threat.keys(), key=lambda c: threat[c]["total"], reverse=True)

    # Total scores leaderboard
    totals = [threat[c]["total"] for c in sorted_companies]
    _add_bar_chart_manual(slide, sorted_companies, totals, "Final Threat Score (/10)",
                          Inches(0.4), Inches(1.1), Inches(4.0), Inches(5.5), ACCENT_PURPLE)

    # Dimension breakdown
    start_x = Inches(5.0)
    dim_y = Inches(1.1)
    _add_text(slide, "SCORE BREAKDOWN", start_x, dim_y - Inches(0.05), W - start_x, Inches(0.28),
              font_size=9, bold=True, color=TEXT_MUTED)
    dim_y += Inches(0.3)

    for c in sorted_companies[:4]:
        _add_text(slide, c[:16], start_x, dim_y, Inches(2.5), Inches(0.3),
                  font_size=10, bold=True, color=ACCENT_PURPLE)
        dim_y += Inches(0.28)
        for dim in dimensions:
            score = threat[c].get(dim, 0)
            bar_w = (score / 10) * Inches(7.8)
            _add_text(slide, dim[:22], start_x, dim_y, Inches(2.0), Inches(0.22),
                      font_size=8, color=TEXT_MUTED)
            _add_rect(slide, start_x + Inches(2.1), dim_y + Inches(0.03), bar_w, Inches(0.15), ACCENT_PURPLE)
            _add_text(slide, str(score), start_x + Inches(2.1) + bar_w + Inches(0.05), dim_y,
                      Inches(0.4), Inches(0.22), font_size=8, color=TEXT_PRIMARY, bold=True)
            dim_y += Inches(0.23)
        dim_y += Inches(0.15)

    # ── SLIDE 9: Strategic AI Recommendations ────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Strategic AI Recommendations", f"Personalized strategy for {user_company}")

    rec_icons = {
        "content_strategy": ("🎯", "Content Strategy", ACCENT_PURPLE),
        "upload_cadence": ("📅", "Upload Cadence", ACCENT_CYAN),
        "shorts_strategy": ("⚡", "Shorts Strategy", ACCENT_PINK),
        "engagement_tips": ("💬", "Engagement Improvement", ACCENT_GREEN),
        "differentiation": ("🚀", "Differentiation Blueprint", ACCENT_AMBER),
    }

    rec_y = Inches(1.1)
    for key, (icon, title, accent) in rec_icons.items():
        text = recs.get(key, "")[:160]
        _add_rect(slide, Inches(0.4), rec_y, Inches(0.06), Inches(0.7), accent)
        _add_text(slide, title, Inches(0.6), rec_y + Inches(0.02), Inches(4), Inches(0.25),
                  font_size=10, bold=True, color=accent)
        _add_text(slide, text, Inches(0.6), rec_y + Inches(0.26), W - Inches(1.0), Inches(0.4),
                  font_size=9, color=TEXT_PRIMARY)
        rec_y += Inches(1.0)

    # ── SLIDE 10: 30-Day Content Roadmap ─────────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "30-Day Content Roadmap", f"Week-by-week execution plan for {user_company}")

    week_colors = [ACCENT_PURPLE, ACCENT_PINK, ACCENT_CYAN, ACCENT_GREEN]
    week_x = [Inches(0.4), Inches(3.6), Inches(6.8), Inches(10.0)]
    week_w = Inches(3.0)

    for i, (week, data) in enumerate(roadmap.items()):
        x = week_x[i]
        _add_rect(slide, x, Inches(1.1), week_w, Inches(5.9), BG_CARD)
        _add_rect(slide, x, Inches(1.1), week_w, Inches(0.05), week_colors[i])
        _add_text(slide, week, x + Inches(0.15), Inches(1.18), week_w - Inches(0.2), Inches(0.28),
                  font_size=11, bold=True, color=week_colors[i])
        _add_text(slide, data["title"], x + Inches(0.15), Inches(1.48), week_w - Inches(0.2), Inches(0.35),
                  font_size=9, bold=True, color=TEXT_PRIMARY)

        action_y = Inches(1.9)
        for action in data["actions"]:
            _add_text(slide, f"→ {action[:55]}", x + Inches(0.15), action_y, week_w - Inches(0.2), Inches(0.38),
                      font_size=8, color=TEXT_MUTED)
            action_y += Inches(0.42)

        _add_text(slide, f"🎯 {data['goal'][:50]}", x + Inches(0.15), Inches(6.65),
                  week_w - Inches(0.2), Inches(0.35), font_size=8, italic=True, color=ACCENT_GREEN)

    # ── SLIDE 11: Viral Pattern Summary ──────────────────────────────────
    slide = _add_slide(prs)
    _add_header_bar(slide, prs, "Viral Pattern Analysis", "What content formats drive outsized performance")

    for i, c in enumerate(companies[:5]):
        v = viral.get(c, {})
        col_x = Inches(0.4) + i * Inches(2.5)
        _add_text(slide, c[:14], col_x, Inches(1.1), Inches(2.4), Inches(0.28),
                  font_size=10, bold=True, color=COLORS_RGB[i % len(COLORS_RGB)])
        ratio = v.get("emotional_vs_promo_ratio", 1)
        best_day = v.get("best_day", "Tue")
        freq = v.get("upload_freq", 4)

        items = [
            ("Emo/Promo Ratio", f"{ratio:.1f}x"),
            ("Best Post Day", best_day),
            ("Posts/Month", str(freq)),
        ]
        for j, (label, val) in enumerate(items):
            _add_kpi_box(slide, label, val, "", col_x, Inches(1.5) + j * Inches(1.7),
                         Inches(2.3), Inches(1.55), accent=COLORS_RGB[i % len(COLORS_RGB)])

    # ── SLIDE 12: Closing / Action Next Steps ─────────────────────────────
    slide = _add_slide(prs)
    _add_rect(slide, 0, 0, W, H, RGBColor(0x0A, 0x08, 0x1A))
    _add_rect(slide, 0, 0, Inches(0.08), H, ACCENT_PINK)

    _add_text(slide, "WHAT TO DO NEXT", Inches(0.6), Inches(1.2), W - Inches(1.2), Inches(0.4),
              font_size=11, bold=True, color=ACCENT_PINK)
    _add_text(slide, "Strategic Action Plan", Inches(0.6), Inches(1.65), W - Inches(1.2), Inches(0.8),
              font_size=32, bold=True, color=TEXT_PRIMARY)

    next_steps = [
        f"01  Prioritize {analytics.whitespace[0]['theme'] if analytics.whitespace else 'Tutorial'} content — highest white space opportunity detected.",
        f"02  Increase upload consistency to {analytics.metrics.get(user_company, {}).get('upload_freq', 4) + 2} videos/month.",
        "03  Launch a 3-part Shorts series this week to boost discovery.",
        "04  Audit top competitor videos and build your counter-strategy.",
        "05  Implement the 30-day roadmap with weekly check-ins.",
    ]

    for i, step in enumerate(next_steps):
        _add_rect(slide, Inches(0.6), Inches(2.7) + i * Inches(0.78), W - Inches(1.2), Inches(0.65),
                  RGBColor(0x0F, 0x12, 0x2A))
        _add_rect(slide, Inches(0.6), Inches(2.7) + i * Inches(0.78), Inches(0.04), Inches(0.65), ACCENT_PURPLE)
        _add_text(slide, step, Inches(0.75), Inches(2.75) + i * Inches(0.78), W - Inches(1.4), Inches(0.55),
                  font_size=11, color=TEXT_PRIMARY)

    _add_text(slide, f"AI Video Marketing War Room · Generated {datetime.now().strftime('%B %Y')}",
              Inches(0.6), Inches(7.1), W - Inches(1.2), Inches(0.28),
              font_size=8, color=TEXT_MUTED)

    # ── Save ──────────────────────────────────────────────────────────────
    buffer = io.BytesIO()
    prs.save(buffer)
    buffer.seek(0)
    return buffer.read()


COLORS_RGB = [ACCENT_PURPLE, ACCENT_PINK, ACCENT_CYAN, ACCENT_GREEN, ACCENT_AMBER]
