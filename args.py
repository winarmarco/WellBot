import argparse
from enum import Enum
from user.user import UserType
from bot.chatbot import BotType


class ArgumentParser:
    def __init__(self):
        # Enhanced argument parser
        self.parser = argparse.ArgumentParser(description="ChatBestie Chat Bot")

        # Add user argument
        self.parser.add_argument(
            "--user",
            type=str,
            choices=[
                t.value for t in UserType
            ],  # This will allow only "json" or "input"
            help="Specify user input type (json or input)",
            default=UserType.INPUT.value,
        )

        # Add user profile path argument
        self.parser.add_argument(
            f"--user_profile",
            type=str,
            help="Path to the user profile JSON file",
        )

        self.parser.add_argument(
            "--bot",
            choices=[t.value for t in BotType],
            default=BotType.INPUT.value,
            help="Bot profile type",
        )

        self.parser.add_argument(
            "--module",
            type=str,
            help="Module name (folder that contains system.txt and tone.txt) when bot=preprompt",
        )
        self.parser.add_argument(
            "--bot_profile",
            type=str,
            help="Path to JSON profile file when bot=predetermined",
        )

        self.parser.add_argument(
            "--export",
            action="store_true",
            help="Export the current session to a json file",
        )
        self.args = self.parser.parse_args()

        # Validate arguments
        if self.args.user == "json" and (not self.args.user_profile):
            self.parser.error("--user_profile argument is required when user=json")
        if self.args.bot == "preprompt" and (not self.args.module):
            self.parser.error("--module argument is required when bot=preprompt")
        if self.args.bot == "json" and not self.args.bot_profile:
            self.parser.error("--bot_profile argument is required when bot=json")

    def get_args(self):
        return self.args
