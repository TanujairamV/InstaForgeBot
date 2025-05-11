from instagrapi import Client
from utils import human_delay, load_config, logging

class Engagement:
    def __init__(self, client: Client):
        self.client = client
        self.config = load_config()

    def like_by_hashtag(self, hashtag: str, amount: int):
        medias = self.client.hashtag_medias_recent(hashtag, amount)
        for media in medias:
            self.client.media_like(media.id)
            logging.info(f"Liked post {media.id} with hashtag #{hashtag}")
            human_delay(5, 10)

    def comment_by_hashtag(self, hashtag: str, amount: int):
        comments = self.config["comments"]
        medias = self.client.hashtag_medias_recent(hashtag, amount)
        for media in medias:
            comment = random.choice(comments)
            self.client.media_comment(media.id, comment)
            logging.info(f"Commented '{comment}' on post {media.id}")
            human_delay(10, 15)

    def follow_by_hashtag(self, hashtag: str, amount: int):
        medias = self.client.hashtag_medias_recent(hashtag, amount)
        for media in medias:
            self.client.user_follow(media.user.pk)
            logging.info(f"Followed user {media.user.username}")
            human_delay(8, 12)

    def unfollow_non_followers(self):
        followers = self.client.user_followers(self.client.user_id)
        following = self.client.user_following(self.client.user_id)
        non_followers = set(following.keys()) - set(followers.keys())
        for user_id in non_followers[:self.config["unfollow_limit"]]:
            self.client.user_unfollow(user_id)
            logging.info(f"Unfollowed user {user_id}")
            human_delay(10, 15)
