from dataclasses import dataclass
from typing import Any
from aiogram import dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from ..additional.func import is_url
from ..additional.stickers import (
    NO_GIRL,
    QUESTION_GIRL,
    OKAY_GIRL,
    TIRED_GIRL,
    YEP_GIRL,
)
from ..storage import engine
from ..config import load_config


config = load_config("config/bot.ini")


@dataclass
class ArticleMenuOptions:
    random_article: str = "Send me a random article!"
    find_article: str = "I want to find article!"
    subscribe: str = "Subscribe me for a daily article"
    cancel: str = "Nope, i wanna go back!"


class ArticlesStates(StatesGroup):
    waiting_for_article_menu_input = State()


def register_handlers_articles(dp: dispatcher):
    dp.register_message_handler(
        call_article_menu,
        commands="articles",
        state="*",
    )
    dp.register_message_handler(
        cancel_article_menu,
        commands="cancel",
        state=ArticlesStates.waiting_for_article_menu_input,
    )
    dp.register_message_handler(
        cancel_article_menu,
        lambda mg: mg.text == ArticleMenuOptions().cancel,
        state=ArticlesStates.waiting_for_article_menu_input,
    )
    dp.register_message_handler(
        add_new_article,
        lambda mg: is_url(mg.text.lower().strip()),
        state="*",
    )


async def call_article_menu(message: types.Message):
    await ArticlesStates.waiting_for_article_menu_input.set()
    menu = ArticleMenuOptions()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        menu.random_article,
        menu.random_article,
        menu.subscribe,
        menu.cancel,
    ]
    keyboard.add(*buttons)
    await message.answer_sticker(
        QUESTION_GIRL,
        reply_markup=keyboard,
    )
    await message.answer("What should I do?", reply_markup=keyboard)


async def cancel_article_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer_sticker(OKAY_GIRL)
    await message.answer(
        "Contact me again later!", reply_markup=types.ReplyKeyboardRemove()
    )


async def add_new_article(message: types.Message, state: FSMContext):
    await state.finish()
    res = None
    try:
        res = engine.add_article(
            config.tg_bot.db_conn_str,
            message.from_user.id,
            message.text.strip().lower(),
        )
    except:
        await message.answer_sticker(NO_GIRL)
        await message.answer(
            "Some problems, mb article is already in database? =(",
            reply_markup=types.ReplyKeyboardRemove(),
        )
    else:
        if res == None:
            await message.answer_sticker(TIRED_GIRL)
            await message.answer(
                "Sorry I didn't find your article...",
                reply_markup=types.ReplyKeyboardRemove(),
            )
        else:
            await message.answer_sticker(YEP_GIRL)
            await message.answer(
                "New article was added:" + res, reply_markup=types.ReplyKeyboardRemove()
            )
