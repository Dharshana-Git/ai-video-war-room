# ⚔️ AI Video Marketing War Room

> A production-grade competitive intelligence platform that analyzes YouTube marketing strategies and generates strategic business insights with downloadable PowerPoint reports.

---

## 🎯 What It Does

The AI Video Marketing War Room lets you enter your company and up to 4 competitors, then automatically:

- Fetches YouTube channel data (subscribers, views, videos, engagement)
- Analyzes content strategy and posting frequency
- Detects content gaps and white-space opportunities
- Scores each brand on 6 competitive dimensions
- Generates AI-powered strategic recommendations
- Exports a premium 12-slide PowerPoint intelligence report

---

## 📐 Architecture

```
ai-video-war-room/
├── app.py                    # Main Streamlit entry point
├── youtube_service.py        # YouTube Data API v3 + demo data fallback
├── analytics_engine.py       # Core business intelligence logic
├── ui_components.py          # All tab renderers + CSS injection
├── ppt_generator.py          # Premium PPTX report generator
├── utils.py                  # Validation + formatting helpers
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .streamlit/
    ├── config.toml           # Dark theme configuration
    └── secrets.toml.template # API key template
```

---

## 🚀 Quick Start (Local)

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd ai-video-war-room
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
YOUTUBE_API_KEY = "AIza..."
GEMINI_API_KEY = "AIza..."
```

> ⚠️ Never commit `secrets.toml` to version control.

### 3. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## 🌐 Deploy to Streamlit Community Cloud

1. Push your code to a **public GitHub repo** (without `secrets.toml`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App** → select your repo → set `app.py` as the main file
4. In **Advanced Settings → Secrets**, paste:
   ```toml
   YOUTUBE_API_KEY = "your_key"
   GEMINI_API_KEY = "your_key"
   ```
5. Deploy 🚀

---

## 🔑 Getting API Keys

### YouTube Data API v3
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create an **API Key** credential
5. (Optional) Restrict it to YouTube Data API

### Gemini API (for AI summaries)
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create an API key
3. Paste into `secrets.toml`

> 💡 **No API keys?** The app runs in **demo mode** with realistic simulated data — perfect for testing and presentations.

---

## 📊 Dashboard Tabs

| Tab | Description |
|-----|-------------|
| 📊 Executive Summary | High-level competitive scorecard and strategic findings |
| 📡 Channel Intelligence | Subscriber counts, videos, upload frequency charts |
| 💥 Engagement | Engagement rates, radar charts, avg views/likes/comments |
| 🎯 AEI Index | Attention Efficiency Index leaderboard and scorecards |
| 🎨 Content Themes | Video topic distribution (Tutorial, Shorts, etc.) |
| 🔥 Viral Patterns | Emotional vs promotional performance, title length analysis |
| 🗺️ White Space Map | Opportunity heatmap of underserved content categories |
| ⚠️ Threat Scoring | 6-dimension competitive threat matrix + leaderboard |
| 🤖 AI Recommendations | Rule-based or Gemini-powered strategic advice |
| 📅 30-Day Roadmap | Week-by-week actionable content plan |

---

## 📥 PowerPoint Export

The **Generate PowerPoint Report** button produces a **12-slide dark-themed intelligence deck**:

1. Title Slide
2. Executive Summary
3. Channel Intelligence
4. Engagement Analysis
5. AEI Index
6. Content Theme Breakdown
7. White Space Opportunity Map
8. Competitive Threat Scoring
9. AI Strategic Recommendations
10. 30-Day Content Roadmap
11. Viral Pattern Summary
12. Next Steps Action Plan

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit + Custom CSS (glassmorphism dark theme) |
| Charts | Plotly |
| YouTube Data | YouTube Data API v3 |
| AI Summaries | Google Gemini 1.5 Flash |
| PPT Generation | python-pptx |
| Deployment | Streamlit Community Cloud |

---

## 🧠 Key Metrics Explained

**Attention Efficiency Index (AEI)**
> `AEI = (Average Views / Subscribers) × 100`
> Measures how effectively a brand converts subscribers into viewers. >30% = high activation.

**Engagement Rate**
> `ER = (Avg Likes + Avg Comments) / Avg Views × 100`
> Normalized engagement metric comparable across brands of different sizes.

**Threat Score**
> Weighted composite of 6 dimensions: Engagement Power, Audience Loyalty, Posting Consistency, SEO Optimization, Content Diversity, Growth Potential.

---

## 🛡️ Notes

- API quota: YouTube Data API v3 has a default quota of 10,000 units/day. Each channel search uses ~100 units.
- Demo mode: Works without any API key using seeded deterministic demo data.
- Rate limiting: App adds small delays between API calls to avoid quota exhaustion.

---
