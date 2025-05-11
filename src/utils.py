import time
import random
import logging
import yaml
from pathlib import Path

logging.basicConfig(
    filename="data/logs/instaforgebot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config():
    config_path = Path("config/config.yaml")
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def load_credentials():
    credentials_path = Path("config/credentials.yaml")
    with open(credentials_path, "r") as file:
        return yaml.safe_load(file)

def human_delay(min_seconds=1, max_seconds=5):
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    logging.info(f"Applied delay of {delay:.2f} seconds")
