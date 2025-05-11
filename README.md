InstaForgeBot
A modular Instagram automation bot with interactive games. For educational purposes only. Use responsibly and comply with Instagram's Terms of Service.
Features

Account Management: Automated account creation, login, proxy support.
Engagement: Auto-like, comment, follow, unfollow based on hashtags or users.
Content: View stories, download posts, schedule posts.
Analytics: Track follower growth, scrape profile data.
Games: Play Trivia, Emoji Story, or Guess the Number with friends via DMs.
Safety: Randomized delays, configurable limits, headless mode.

Installation

Clone the repository:git clone https://github.com/yourusername/InstaForgeBot.git
cd InstaForgeBot


Install dependencies:pip install -r requirements.txt


Install ChromeDriver for Selenium (ensure it matches your Chrome version).
Configure config/credentials.yaml with your Instagram credentials.
Configure config/config.yaml with your preferences.

Usage
Run the bot:
python src/main.py

Games
Play with friends via Instagram DMs by sending commands:

!trivia <category>: Start a trivia game (e.g., !trivia history).
!emojistory <turns>: Build an emoji story (e.g., !emojistory 5).
!guessnumber: Guess a number between 1 and 100.

Configuration

config/credentials.yaml: Store your Instagram username and password.
config/config.yaml: Customize bot behavior (e.g., enable games, set hashtags).

Directory Structure
InstaForgeBot/
├── src/                    # Source code
├── config/                 # Configuration files
├── data/                   # Logs, downloads, analytics
├── tests/                  # Unit tests
├── requirements.txt        # Dependencies
├── README.md               # Documentation
└── .gitignore              # Git ignore file

Disclaimer
This project is for educational purposes only. Unauthorized automation violates Instagram’s Terms of Service and may result in account bans or legal action. Use at your own risk.
Contributing
Pull requests are welcome! Please open an issue to discuss major changes.
License
MIT License
