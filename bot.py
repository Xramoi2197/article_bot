import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand

from app.config import load_config
from app.handlers.common import register_handlers_common
from app.handlers.articles import register_handlers_articles

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/articles", description="Articles"),
        BotCommand(command="/more", description="More"),
        BotCommand(command="/help", description="Help"),
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    config = load_config("config/bot.ini")

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    register_handlers_common(dp)
    register_handlers_articles(dp)

    await set_commands(bot)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
