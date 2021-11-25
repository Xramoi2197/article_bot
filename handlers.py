from aiogram import types

def greeting(message: types.message) -> str:
    return f"Hi, {message.from_user.get_mention(as_html=True)}!\nI'm EchoBot!\nPowered by aiogram."
    