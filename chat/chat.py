from bot.chatbot import Bot, BotUtils
from user.user import User
from termcolor import colored
from datetime import datetime
import json
import os


class Chat:
    conversations: list[dict] = []
    user: User
    bot: Bot

    def __init__(self, bot: Bot, user: User, other_instructions: list[dict] = []):
        self.user = user
        self.bot = bot
        self.conversations = []

        self.conversations.append(
            {"role": "system", "content": bot.get_prompt_collection().system_prompt}
        )
        self.conversations.append(
            {"role": "system", "content": bot.get_prompt_collection().tone_prompt}
        )

        for instruction in other_instructions:
            self.conversations.append(instruction)

    def start_chat(self):
        bot_utils = BotUtils()
        user_name = self.user.get_profile().full_name
        bot_name = self.bot.get_profile().name
        while True:
            # 1. Get User input
            user_input = input(colored(f"{user_name}: ", "yellow"))
            print()

            # Check if user wants to exit chat session
            if user_input.lower() == "exit":
                break

            self.conversations.append(
                {
                    "role": "user",
                    "content": user_input,
                },
            )

            # 2. Get Bot Reply
            bot_response = bot_utils.get_chat_completion(message=self.conversations)

            self.conversations.append({"role": "assistant", "content": bot_response})

            bot_response_bubbles = bot_response.split("\n\n")

            for bubble in bot_response_bubbles:
                if bubble:
                    print(
                        colored(f"{bot_name if bot_name else 'Bestie'} :", "green"),
                        bubble,
                    )
                    print()

        print("Chat Session Ended")
        return self.conversations

    def export(self, path: str = None):
        # Export all the chat-session, including, user, bot, and data
        if path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"output/chat_{timestamp}"

        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)
        self.user.export(f"{path}/user.json")
        self.bot.export(f"{path}/bot.json")

        with open(f"{path}/conversation.json", "w", encoding="utf-8") as file:
            data = {"conversations": self.conversations}
            json.dump(data, file, indent=4, ensure_ascii=False)
