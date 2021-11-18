import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types

from private import ARTICLE_BOT_KEY, TELEGRAM_ID

logging.basicConfig(level=logging.INFO)
bot = Bot(token=ARTICLE_BOT_KEY)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start", "help", "restart"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        f"Hi, {message.from_user.get_mention(as_html=True)}!\nI'm EchoBot!\nPowered by aiogram.",
        parse_mode=types.ParseMode.HTML,
    )


@dp.message_handler(commands="test")
async def cmd_test(message: types.Message):
    await message.reply("text")


@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
