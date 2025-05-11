from instagrapi import Client
import random
import time
from utils import human_delay, load_config, logging

class GameManager:
    def __init__(self, client: Client):
        self.client = client
        self.config = load_config()
        self.trivia_db = {
            "history": [
                {"question": "Who was the first U.S. President?", "answer": "George Washington"},
                {"question": "In which year did WW2 end?", "answer": "1945"}
            ],
            "science": [
                {"question": "What is the chemical symbol for water?", "answer": "H2O"},
                {"question": "What planet is closest to the sun?", "answer": "Mercury"}
            ]
        }
        self.game_states = {}

    def monitor_dms(self):
        while True:
            threads = self.client.direct_threads(20)
            for thread in threads:
                self._process_thread(thread)
            human_delay(30, 60)

    def _process_thread(self, thread):
        thread_id = thread.id
        messages = thread.messages
        for message in messages:
            if message.user_id == self.client.user_id:
                continue
            text = message.text.lower() if message.text else ""
            if text.startswith("!trivia"):
                self._start_trivia(thread_id, text, message.user_id)
            elif text.startswith("!emojistory"):
                self._start_emoji_story(thread_id, text, message.user_id)
            elif text.startswith("!guessnumber"):
                self._start_guess_number(thread_id, message.user_id)
            elif thread_id in self.game_states:
                self._handle_game_response(thread_id, text, message.user_id)

    def _start_trivia(self, thread_id, command, user_id):
        parts = command.split()
        category = parts[1] if len(parts) > 1 and parts[1] in self.trivia_db else random.choice(list(self.trivia_db.keys()))
        question_data = random.choice(self.trivia_db[category])
        self.game_states[thread_id] = {
            "type": "trivia",
            "question": question_data["question"],
            "answer": question_data["answer"].lower(),
            "scores": {str(user_id): 0},
            "current_player": user_id
        }
        self.client.direct_send(f"Trivia: {question_data['question']}", thread_ids=[thread_id])
        logging.info(f"Started trivia in thread {thread_id}")

    def _start_emoji_story(self, thread_id, command, user_id):
        parts = command.split()
        turns = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
        self.game_states[thread_id] = {
            "type": "emojistory",
            "story": [],
            "turns_left": turns,
            "players": [user_id],
            "current_player": user_id
        }
        self.client.direct_send("Emoji Story: Add one emoji to start the story!", thread_ids=[thread_id])
        logging.info(f"Started emoji story in thread {thread_id}")

    def _start_guess_number(self, thread_id, user_id):
        self.game_states[thread_id] = {
            "type": "guessnumber",
            "number": random.randint(1, 100),
            "attempts": 0,
            "current_player": user_id
        }
        self.client.direct_send("Guess the Number (1-100): Send your guess!", thread_ids=[thread_id])
        logging.info(f"Started guess number in thread {thread_id}")

    def _handle_game_response(self, thread_id, text, user_id):
        state = self.game_states[thread_id]
        if state["type"] == "trivia" and user_id == state["current_player"]:
            if text.lower() == state["answer"]:
                state["scores"][str(user_id)] += 1
                self.client.direct_send(f"Correct! Score: {state['scores'][str(user_id)]}. Want another? Send !trivia", thread_ids=[thread_id])
                del self.game_states[thread_id]
            else:
                self.client.direct_send("Wrong! Try again or send !trivia for a new question", thread_ids=[thread_id])
            logging.info(f"Trivia response in thread {thread_id}: {text}")
        
        elif state["type"] == "emojistory" and user_id in state["players"]:
            if len(text) <= 2:
                state["story"].append(text)
                state["turns_left"] -= 1
                if state["turns_left"] == 0:
                    self.client.direct_send(f"Story complete: {' '.join(state['story'])}", thread_ids=[thread_id])
                    del self.game_states[thread_id]
                else:
                    self.client.direct_send(f"Story so far: {' '.join(state['story'])}. Next player, add an emoji!", thread_ids=[thread_id])
                logging.info(f"Emoji story update in thread {thread_id}: {text}")
        
        elif state["type"] == "guessnumber" and user_id == state["current_player"]:
            try:
                guess = int(text)
                state["attempts"] += 1
                if guess == state["number"]:
                    self.client.direct_send(f"Correct! You got it in {state['attempts']} attempts!", thread_ids=[thread_id])
                    del self.game_states[thread_id]
                elif guess < state["number"]:
                    self.client.direct_send("Too low! Guess again", thread_ids=[thread_id])
                else:
                    self.client.direct_send("Too high! Guess again", thread_ids=[thread_id])
                logging.info(f"Guess number response in thread {thread_id}: {guess}")
            except ValueError:
                self.client.direct_send("Please send a number!", thread_ids=[thread_id])
