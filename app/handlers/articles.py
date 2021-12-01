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


def register_handlers_articles(dp: dispatcher):
    articles_menu = ArticleMenuOptions()
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
        lambda mg: mg.text == articles_menu.cancel,
        state=ArticlesStates.waiting_for_article_menu_input,
    )
    dp.register_message_handler(
        add_new_article,
        lambda mg: is_url(mg.text.lower().strip()),
        state="*",
    )
    dp.register_message_handler(
        list_all_articles,
        lambda mg: mg.text == articles_menu.list_articles,
        state=ArticlesStates.waiting_for_article_menu_input,
    )
    dp.register_callback_query_handler(
        callback_articles_pagination,
        lambda c: "page_button" in c.data,
    )


async def call_article_menu(message: types.Message):
    await ArticlesStates.waiting_for_article_menu_input.set()
    menu = ArticleMenuOptions()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        menu.list_articles,
        # menu.list_articles,
        # menu.subscribe,
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
    page = 1
    db_engine = engine.create_engine(config.tg_bot.db_conn_str)
    lst = engine.get_articles_page(db_engine, message.from_user.id, page)
    next_lst = engine.get_articles_page(db_engine, message.from_user.id, page + 1)
    inline_buttons = types.InlineKeyboardMarkup()
    if len(lst) == 0:
        await message.answer_sticker(
            TIRED_GIRL, reply_markup=types.ReplyKeyboardRemove()
        )
        await message.answer("I didn't find any articles in database(")
        await state.finish()
    else:
        if len(next_lst) > 0:
            inline_btn_next = types.InlineKeyboardButton(
                "Next", callback_data="page_button?" + str(page + 1)
            )
            inline_buttons.add(inline_btn_next)
        message_text = "\n".join(
            [f"<a href='{article[1]}'>{article[0]}</a>" for article in lst]
        )
        await message.answer_sticker(
            OKAY_GIRL, reply_markup=types.ReplyKeyboardRemove()
        )
        await state.finish()
        await message.answer(
            message_text,
            parse_mode=types.ParseMode.HTML,
            reply_markup=inline_buttons,
        )


async def callback_articles_pagination(call: types.CallbackQuery):
    page = int(call.data.split("?")[1])
    db_engine = engine.create_engine(config.tg_bot.db_conn_str)
    lst = engine.get_articles_page(db_engine, call.from_user.id, page)
    next_lst = engine.get_articles_page(db_engine, call.from_user.id, page + 1)
    inline_buttons = types.InlineKeyboardMarkup()
    if len(lst) == 0:
        await call.message.edit_text("I didn't find any articles in database(")
    else:
        if page != 1:
            inline_btn_previous = types.InlineKeyboardButton(
                "Previous", callback_data="page_button?" + str(page - 1)
            )
            inline_buttons.insert(inline_btn_previous)
        if len(next_lst) > 0:
            inline_btn_next = types.InlineKeyboardButton(
                "Next", callback_data="page_button?" + str(page + 1)
            )
            inline_buttons.insert(inline_btn_next)
        message_text = "\n".join(
            [f"<a href='{article[1]}'>{article[0]}</a>" for article in lst]
        )
        await call.message.edit_text(
            message_text,
            parse_mode=types.ParseMode.HTML,
            reply_markup=inline_buttons,
        )
