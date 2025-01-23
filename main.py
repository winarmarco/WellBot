from args import ArgumentParser
from user.user import UserReader
from bot.chatbot import BotReader
from chat.chat import Chat
from termcolor import colored
from utils import get_contact_psychologist
import env

if __name__ == "__main__":
    # 1. Get Arguments
    arguments = ArgumentParser().get_args()

    # 2. Get User profile based on arguments
    user = UserReader(arguments).get_user()

    # 3. Get Bot Profile based on arguments
    bot = BotReader(arguments).get_bot()

    # 4. Create Chatbot
    bot.create(user=user)

    # 5. Start conversation
    chat = Chat(
        bot=bot,
        user=user,
        other_instructions=[{"role": "system", "content": get_contact_psychologist()}],
    )
    chat.start_chat()

    # 6. Save conversation
    if hasattr(arguments, "export") and arguments.export:
        chat.export()
