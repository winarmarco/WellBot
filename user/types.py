from dataclasses import dataclass, asdict, fields
from enum import Enum


class UserType(Enum):
    JSON = "json"
    INPUT = "input"


@dataclass
class _UserProfile:
    full_name: str = ""
    nickname: str = ""
    age: str = ""
    gender: str = ""

    def __str__(self):
        return "\n".join(
            f"{key.replace('_', ' ').capitalize()}: {value}"
            for key, value in asdict(self).items()
        )
