from instagrapi import Client
import pandas as pd
from datetime import datetime
from utils import logging
from pathlib import Path

class Analytics:
    def __init__(self, client: Client):
        self.client = client

    def track_followers(self, username: str):
        user_id = self.client.user_id_from_username(username)
        user_info = self.client.user_info(user_id)
        data = {
            "timestamp": datetime.now(),
            "username": username,
            "followers": user_info.follower_count,
            "following": user_info.following_count,
            "posts": user_info.media_count
        }
        df = pd.DataFrame([data])
        output_path = Path("data/analytics/follower_data.csv")
        if output_path.exists():
            df.to_csv(output_path, mode="a", header=False, index=False)
        else:
            df.to_csv(output_path, index=False)
        logging.info(f"Tracked analytics for {username}: {data}")

    def scrape_profile(self, username: str):
        user_id = self.client.user_id_from_username(username)
        user_info = self.client.user_info(user_id)
        data = {
            "username": user_info.username,
            "full_name": user_info.full_name,
            "bio": user_info.biography,
            "followers": user_info.follower_count,
            "following": user_info.following_count,
            "posts": user_info.media_count,
            "is_private": user_info.is_private
        }
        logging.info(f"Scraped profile data for {username}")
        return data
