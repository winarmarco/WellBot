from argparse import Namespace
from dataclasses import dataclass, asdict, fields
import json
from datetime import datetime
from user.types import _UserProfile, UserType


class User:
    _user_profile: _UserProfile

    def __init__(self, user_type: UserType):
        self.user_type = user_type
        self._user_profile = _UserProfile()

    def set_profile(self, user_profile: _UserProfile):
        self._user_profile = user_profile

    def get_profile(self) -> _UserProfile:
        return self._user_profile

    def export(self, export_path: str = None):
        # By default export will go to user-profile-<timestamp>.json
        if export_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = f"user-profile-{timestamp}.json"

        profile_data = asdict(self._user_profile)

        with open(export_path, "w", encoding="utf-8") as file:
            json.dump(profile_data, file, indent=4, ensure_ascii=False)

    def __str__(self):
        return (
            f"Full Name: {self._user_profile.full_name}\n"
            f"Nickname: {self._user_profile.nickname}\n"
            f"Age: {self._user_profile.age}\n"
            f"Gender: {self._user_profile.gender}"
        )


class JsonUser(User):
    def __init__(self, json_file: str):
        super().__init__(UserType.JSON)
        self._read_profile_json(json_file)

    def _read_profile_json(self, json_file: str):
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
                # Dynamically map JSON keys to _UserProfile fields
                profile_data = {
                    field.name: data.get(
                        field.name, getattr(_UserProfile(), field.name)
                    )
                    for field in fields(_UserProfile)
                }
                user_profile = _UserProfile(**profile_data)
                self.set_profile(user_profile)
        except FileNotFoundError:
            raise ValueError(f"JSON file '{json_file}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from file '{json_file}'.")


class InputUser(User):
    def __init__(self):
        super().__init__(UserType.INPUT)
        self._get_profile_input()

    def _get_profile_input(self):
        print("USER PROFILE")
        print("=" * 30)
        profile_data = {
            "full_name": input("Enter full name: "),
            "nickname": input("Enter nickname: "),
            "age": input("Enter age: "),
            "gender": input("Enter gender: "),
        }
        user_profile = _UserProfile(**profile_data)
        self.set_profile(user_profile)


class UserReader:
    def __init__(self, arguments: Namespace) -> None:
        self.arguments = arguments

    def get_user(self) -> User:
        user_type = UserType(self.arguments.user)

        if user_type == UserType.JSON:
            if not hasattr(self.arguments, "user_profile"):
                raise ValueError("--user_profile is required for JSON user type")
            return JsonUser(self.arguments.user_profile)

        if user_type == UserType.INPUT:
            return InputUser()

        raise ValueError(f"Unknown user type: {user_type}")
