from account_manager import AccountManager
from engagement import Engagement
from content import ContentManager
from analytics import Analytics
from games import GameManager
from utils import load_config, load_credentials, logging

def main():
    config = load_config()
    credentials = load_credentials()
    account = AccountManager(credentials)
    
    if config["create_account"]:
        account.create_account()
    else:
        account.login()
    
    engagement = Engagement(account.client)
    content = ContentManager(account.client)
    analytics = Analytics(account.client)
    games = GameManager(account.client)
    
    if config["engagement"]["like"]:
        engagement.like_by_hashtag(config["engagement"]["hashtag"], config["engagement"]["like_amount"])
    if config["engagement"]["comment"]:
        engagement.comment_by_hashtag(config["engagement"]["hashtag"], config["engagement"]["comment_amount"])
    if config["engagement"]["follow"]:
        engagement.follow_by_hashtag(config["engagement"]["hashtag"], config["engagement"]["follow_amount"])
    if config["engagement"]["unfollow"]:
        engagement.unfollow_non_followers()
    
    if config["content"]["view_stories"]:
        content.view_stories(config["content"]["target_user"])
    if config["content"]["download_post"]:
        content.download_post(config["content"]["post_url"])
    if config["content"]["schedule_post"]:
        content.schedule_post(
            config["content"]["image_path"],
            config["content"]["caption"],
            config["content"]["post_time"]
        )
        content.run_scheduler()
    
    if config["analytics"]["track_followers"]:
        analytics.track_followers(credentials["username"])
    if config["analytics"]["scrape_profile"]:
        profile_data = analytics.scrape_profile(config["analytics"]["target_user"])
        logging.info(f"Profile data: {profile_data}")
    
    if config["games"]["enabled"]:
        games.monitor_dms()

if __name__ == "__main__":
    main()
