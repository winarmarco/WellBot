from dataclasses import dataclass, asdict, fields
from enum import Enum


class BotType(Enum):
    INPUT = "input"
    JSON = "json"
    PREPROMPT = "preprompt"


@dataclass
class _BotProfile:
    name: str = ""
    role: str = ""
    description: str = ""
    gender: str = ""
    communication_style: str = ""
    nickname: str = ""
    language: str = ""
    personality: str = ""

    def __str__(self):
        return "\n".join(
            f"{key.replace('_', ' ').capitalize()}: {value}"
            for key, value in asdict(self).items()
        )


@dataclass
class _BotPrompt:
    system_prompt: str = ""
    tone_prompt: str = ""
