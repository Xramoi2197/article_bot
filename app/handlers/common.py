from aiogram import dispatcher, types

def register_handlers_common(dp: dispatcher):
    dp.register_message_handler(greeting, commands=["start", "help", "restart"])

def greeting(message: types.message) -> str:
    return f"Hi, {message.from_user.get_mention(as_html=True)}!\nI'm EchoBot!\nPowered by aiogram."
    