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
    list_articles: str = "List all articles!"
    find_article: str = "I want to find article!"
    subscribe: str = "Subscribe me for a daily article"
    cancel: str = "Nope, i wanna go back!"


class ArticlesStates(StatesGroup):
    waiting_for_article_menu_input = State()
    list_articles_state = State()


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
    dp.register_message_handler(
        list_all_articles,
        lambda mg: mg.text == ArticleMenuOptions().list_articles,
        state=ArticlesStates.waiting_for_article_menu_input,
    )


async def call_article_menu(message: types.Message):
    await ArticlesStates.waiting_for_article_menu_input.set()
    menu = ArticleMenuOptions()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        menu.list_articles,
        menu.list_articles,
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
        db_engine = engine.create_engine(config.tg_bot.db_conn_str)
        res = engine.add_article(
            db_engine,
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


async def list_all_articles(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    page = None
    if "page" not in user_data.keys():
        await ArticlesStates.list_articles_state.set()
        page = 1
        await state.update_data(page=page)
    else:
        page = user_data["page"]
    db_engine = engine.create_engine(config.tg_bot.db_conn_str)
    lst = engine.get_articles_page(db_engine, message.from_user.id, page)
    res = len(lst)
    await message.answer(
        "List len: " + str(res), reply_markup=types.ReplyKeyboardRemove()
    )
    await state.finish()
