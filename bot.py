import asyncio
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.bot_command import BotCommand

from config.private import ARTICLE_BOT_KEY
import app.handlers.common as cmn

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/help", description="Помощь"),
        # BotCommand(command="/food", description="Заказать блюда"),
        # BotCommand(command="/cancel", description="Отменить текущее действие"),
    ]
    await bot.set_my_commands(commands)


# @dp.message_handler(commands=["start", "help", "restart"])
# async def send_greeting(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ["С пюрешкой", "Без пюрешки"]
#     keyboard.add(*buttons)
#     await message.reply(cmn.greeting(message=message), parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


# @dp.message_handler(commands="dice")
# async def cmd_dice(message: types.Message):
#     await message.answer_dice(emoji="🎲")


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    bot = Bot(token=ARTICLE_BOT_KEY)
    dp = Dispatcher(bot=bot)

    await set_commands(bot)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
