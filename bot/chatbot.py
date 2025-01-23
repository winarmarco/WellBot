from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import asdict, fields
from argparse import Namespace
import json
from datetime import datetime
from user.user import User
from bot.utils import BotUtils
from bot.types import _BotProfile, _BotPrompt, BotType


class Bot(ABC):
    _bot_profile: _BotProfile
    _bot_prompts: _BotPrompt
    _bot_utils: BotUtils

    def __init__(self, bot_type: BotType):
        self.bot_type: BotType = bot_type
        self._bot_profile = _BotProfile()
        self._bot_prompts = _BotPrompt()
        self._bot_utils = BotUtils()

    def set_profile(self, bot_profile: _BotProfile):
        self._bot_profile = bot_profile

    def set_prompt_collection(self, bot_prompts: _BotPrompt):
        # Set prompt collections
        self._bot_prompts = bot_prompts

    def get_profile(self):
        return self._bot_profile

    def get_prompt_collection(self):
        return self._bot_prompts

    def create(self, user: User):
        # Get system prompt and assign the system prompts
        if self.bot_type == BotType.PREPROMPT:
            return
        system_prompt = self._bot_utils.get_system_prompt(
            bot_profile=self.get_profile(), user_profile=user.get_profile()
        )
        tone_prompt = self._bot_utils.get_tone_prompt(
            bot_profile=self.get_profile(), user_profile=user.get_profile()
        )

        self.set_prompt_collection(
            _BotPrompt(system_prompt=system_prompt, tone_prompt=tone_prompt)
        )

    def export(self, export_path: str = None):
        if export_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"bot-profile-{timestamp}.json"

        profile: _BotProfile = self.get_profile()
        prompts: _BotPrompt = self.get_prompt_collection()

        # Serialize the profile and prompt into a JSON structure
        data = {
            "type": self.bot_type.value,
            "profile": asdict(profile),
            "prompt": asdict(prompts),
        }

        # Write to a JSON file
        with open(export_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


class InputBot(Bot):
    def __init__(self):
        super().__init__(BotType.INPUT)
        self._get_profile_input()

    def _get_profile_input(self):
        # Collect user input for each field in the bot profile
        bot_profile = _BotProfile(
            name=input("Enter bot name: "),
            role=input("Enter bot role: "),
            description=input("Enter bot description: "),
            gender=input("Enter bot gender: "),
            communication_style=input("Enter bot communication style: "),
            nickname=input("Enter bot nickname: "),
            language=input("Enter bot language: "),
            personality=input("Enter bot personality: "),
        )
        self.set_profile(bot_profile=bot_profile)


class JsonBot(Bot):
    def __init__(self, json_file: str):
        super().__init__(BotType.JSON)
        self._read_profile_json(json_file)

    def _read_profile_json(self, json_file):
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
                # Dynamically map keys from JSON to _BotProfile fields
                bot_profile_data = {
                    field.name: data.get(field.name, getattr(_BotProfile(), field.name))
                    for field in fields(_BotProfile)
                }
                bot_profile = _BotProfile(**bot_profile_data)
                self.set_profile(bot_profile=bot_profile)
        except FileNotFoundError:
            raise ValueError(f"JSON file '{json_file}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from file '{json_file}'.")


class PrepromptBot(Bot):
    def __init__(self, module: str):
        super().__init__(BotType.PREPROMPT)
        self._read_prompt_module(module)

    def _read_prompt_module(self, module: str):
        try:
            with open(f"{module}/system.txt", "r") as system_file:
                system_prompt = system_file.read()
            with open(f"{module}/tone.txt", "r") as tone_file:
                tone_prompt = tone_file.read()
            bot_prompts = _BotPrompt(
                system_prompt=system_prompt, tone_prompt=tone_prompt
            )
            self.set_prompt_collection(bot_prompts=bot_prompts)
        except FileNotFoundError as e:
            raise ValueError(f"Error: {e.filename} not found.")


class BotReader:
    def __init__(self, arguments: Namespace) -> None:
        self.arguments = arguments

    def get_bot(self) -> Bot:
        bot_type = BotType(self.arguments.bot)

        if bot_type == BotType.JSON:
            if not hasattr(self.arguments, "bot_profile"):
                raise ValueError("--bot_profile is required for JSON bot type")
            return JsonBot(self.arguments.bot_profile)

        if bot_type == BotType.PREPROMPT:
            if not hasattr(self.arguments, "module"):
                raise ValueError("--module is required for PREPROMPT bot type")
            return PrepromptBot(module=self.arguments.module)

        if bot_type == BotType.INPUT:
            return InputBot()

        raise ValueError(f"Unknown bot type: {bot_type}")
