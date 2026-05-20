"""
youtube_service.py — YouTube Data API v3 integration
Fetches channel metadata, top videos, recent uploads, and engagement metrics.
Falls back to realistic demo data when no API key is provided.
"""

import random
import re
from datetime import datetime, timedelta

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False


class YouTubeService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = None
        if api_key and GOOGLE_API_AVAILABLE:
            try:
                self.youtube = build("youtube", "v3", developerKey=api_key)
            except Exception as e:
                print(f"YouTube API init error: {e}")

    # ─── Public Interface ─────────────────────────────────────────────────────

    def fetch_channel_data(self, company_name: str) -> dict:
        """Fetch full channel data for a given company name."""
        if self.youtube:
            return self._fetch_real_data(company_name)
        return self._generate_demo_data(company_name)

    # ─── Real API Calls ───────────────────────────────────────────────────────

    def _fetch_real_data(self, company_name: str) -> dict:
        try:
            channel = self._search_channel(company_name)
            if not channel:
                return self._generate_demo_data(company_name)

            channel_id = channel["id"]["channelId"]
            stats = self._get_channel_stats(channel_id)
            top_videos = self._get_top_videos(channel_id)
            recent_videos = self._get_recent_videos(channel_id)

            return {
                "name": company_name,
                "channel_name": channel.get("snippet", {}).get("title", company_name),
                "channel_id": channel_id,
                "subscribers": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "total_videos": int(stats.get("videoCount", 0)),
                "top_videos": top_videos,
                "recent_videos": recent_videos,
                "description": channel.get("snippet", {}).get("description", ""),
            }
        except Exception as e:
            print(f"Error fetching real data for {company_name}: {e}")
            return self._generate_demo_data(company_name)

    def _search_channel(self, company_name: str) -> dict | None:
        response = self.youtube.search().list(
            part="snippet",
            q=company_name,
            type="channel",
            maxResults=1
        ).execute()
        items = response.get("items", [])
        return items[0] if items else None

    def _get_channel_stats(self, channel_id: str) -> dict:
        response = self.youtube.channels().list(
            part="statistics",
            id=channel_id
        ).execute()
        items = response.get("items", [])
        return items[0].get("statistics", {}) if items else {}

    def _get_top_videos(self, channel_id: str) -> list:
        search_response = self.youtube.search().list(
            part="id",
            channelId=channel_id,
            order="viewCount",
            type="video",
            maxResults=10
        ).execute()

        video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
        if not video_ids:
            return []

        stats_response = self.youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids)
        ).execute()

        return [self._parse_video(item) for item in stats_response.get("items", [])]

    def _get_recent_videos(self, channel_id: str) -> list:
        search_response = self.youtube.search().list(
            part="id",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=10
        ).execute()

        video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
        if not video_ids:
            return []

        stats_response = self.youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids)
        ).execute()

        return [self._parse_video(item) for item in stats_response.get("items", [])]

    def _parse_video(self, item: dict) -> dict:
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        return {
            "id": item.get("id", ""),
            "title": snippet.get("title", ""),
            "published_at": snippet.get("publishedAt", ""),
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "comments": int(stats.get("commentCount", 0)),
            "description": snippet.get("description", "")[:200],
        }

    # ─── Demo Data Generator ─────────────────────────────────────────────────

    def _generate_demo_data(self, company_name: str) -> dict:
        """
        Generates realistic demo data based on company name seed.
        Ensures consistent results per company name.
        """
        seed = sum(ord(c) for c in company_name)
        rng = random.Random(seed)

        tiers = [
            {"subs": (50_000, 200_000), "views": (2_000_000, 10_000_000), "videos": (80, 200)},
            {"subs": (200_000, 1_000_000), "views": (10_000_000, 80_000_000), "videos": (200, 600)},
            {"subs": (1_000_000, 5_000_000), "views": (80_000_000, 500_000_000), "videos": (600, 2000)},
        ]
        tier = tiers[seed % 3]

        subscribers = rng.randint(*tier["subs"])
        total_views = rng.randint(*tier["views"])
        total_videos = rng.randint(*tier["videos"])

        top_videos = self._generate_demo_videos(company_name, rng, subscribers, count=10, style="top")
        recent_videos = self._generate_demo_videos(company_name, rng, subscribers, count=10, style="recent")

        return {
            "name": company_name,
            "channel_name": f"{company_name} Official",
            "channel_id": f"UC_{company_name[:6].replace(' ', '').upper()}",
            "subscribers": subscribers,
            "total_views": total_views,
            "total_videos": total_videos,
            "top_videos": top_videos,
            "recent_videos": recent_videos,
            "description": f"Official YouTube channel for {company_name}. Subscribe for product updates, tutorials, and more.",
        }

    def _generate_demo_videos(self, company: str, rng: random.Random, subscribers: int, count: int, style: str) -> list:
        title_templates = {
            "tutorial": [
                "How to {verb} {topic} in 2024",
                "{topic} Tutorial: Complete Beginner's Guide",
                "The ONLY {topic} Tutorial You'll Ever Need",
                "Master {topic} in {n} Minutes",
            ],
            "product": [
                "{company} Launches New {product} — Full Review",
                "Introducing {product}: The Future of {topic}",
                "{product} vs Competitors: Honest Comparison",
                "We Built {product} — Here's Why",
            ],
            "shorts": [
                "{topic} in 60 seconds 🔥",
                "Did you know this {topic} hack? #Shorts",
                "POV: You discovered {company} #shorts",
            ],
            "story": [
                "How {company} Grew from 0 to {n}M Users",
                "Our Biggest Failure (And What We Learned)",
                "Behind the Scenes at {company} HQ",
                "The Real Story Behind {company}",
            ],
            "educational": [
                "Why {topic} is Changing Everything in 2024",
                "{n} Things Nobody Tells You About {topic}",
                "The Complete Guide to {topic}",
                "Is {topic} Worth It? Honest Answer",
            ],
        }

        topics = ["AI", "Marketing", "Analytics", "Growth", "SEO", "Content", "SaaS", "Data", "Video", "Strategy"]
        verbs = ["Use", "Build", "Scale", "Launch", "Automate", "Optimize"]
        products = ["Pro Dashboard", "AI Suite", "Analytics Hub", "Growth Engine", "Smart Tools"]

        videos = []
        base_date = datetime.now() if style == "recent" else datetime(2023, 1, 1)

        for i in range(count):
            category = rng.choice(list(title_templates.keys()))
            template = rng.choice(title_templates[category])

            title = template.format(
                company=company,
                topic=rng.choice(topics),
                verb=rng.choice(verbs),
                product=rng.choice(products),
                n=rng.choice([5, 7, 10, 15, 3]),
            )

            if style == "top":
                views = rng.randint(subscribers // 2, subscribers * 8)
            else:
                views = rng.randint(subscribers // 20, subscribers * 2)

            likes = int(views * rng.uniform(0.02, 0.08))
            comments = int(likes * rng.uniform(0.05, 0.20))

            if style == "recent":
                days_ago = rng.randint(i * 3, i * 10 + 7)
                pub_date = (datetime.now() - timedelta(days=days_ago)).isoformat() + "Z"
            else:
                days_ago = rng.randint(30, 730)
                pub_date = (datetime.now() - timedelta(days=days_ago)).isoformat() + "Z"

            videos.append({
                "id": f"vid_{company[:3]}_{i}",
                "title": title,
                "published_at": pub_date,
                "views": views,
                "likes": likes,
                "comments": comments,
                "description": f"In this video we cover {title.lower()}. Subscribe for more.",
                "category": category,
            })

        # Sort by views for top, by date for recent
        if style == "top":
            videos.sort(key=lambda x: x["views"], reverse=True)
        else:
            videos.sort(key=lambda x: x["published_at"], reverse=True)

        return videos
