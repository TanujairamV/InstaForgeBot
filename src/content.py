from instagrapi import Client
import schedule
import time
from utils import human_delay, load_config, logging
from pathlib import Path

class ContentManager:
    def __init__(self, client: Client):
        self.client = client
        self.config = load_config()

    def view_stories(self, username: str):
        user_id = self.client.user_id_from_username(username)
        stories = self.client.user_stories(user_id)
        for story in stories:
            self.client.story_view(story.pk)
            logging.info(f"Viewed story {story.pk} from {username}")
            human_delay(2, 4)

    def download_post(self, url: str, save_path: str = "data/downloads"):
        media_id = self.client.media_id(self.client.media_pk_from_url(url))
        media = self.client.media_info(media_id)
        path = Path(save_path) / f"{media.id}.{media.media_type}"
        self.client.download_photo(media.thumbnail_url, path) if media.media_type == "photo" else self.client.download_video(media.video_url, path)
        logging.info(f"Downloaded post {media.id} to {path}")
        return path

    def schedule_post(self, image_path: str, caption: str, post_time: str):
        def post_job():
            self.client.photo_upload(image_path, caption)
            logging.info(f"Posted image {image_path} with caption: {caption}")
        schedule.every().day.at(post_time).do(post_job)
        logging.info(f"Scheduled post at {post_time}")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(60)
