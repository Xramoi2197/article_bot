from dataclasses import dataclass
from typing import Text
from aiogram import dispatcher, types
from aiogram.dispatcher import FSMContext, storage
from aiogram.dispatcher.filters.state import State, StatesGroup

from ..accessory import is_url


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
        r"CAACAgIAAxkBAAEDXxdhofbcBUKd9TAnn-vA7miyagVjMwACqQwAAsKEqEuk98oo6Ftp5CIE",
        reply_markup=keyboard,
    )
    await message.answer("What should I do?", reply_markup=keyboard)


async def cancel_article_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer_sticker(
        r"CAACAgIAAxkBAAEDXythohby9ypCz9ZYNOdHapZ8isG5GgACpw8AAmwCsEuGHNhMS20YAAEiBA"
    )
    await message.answer(
        "Contact me again later!", reply_markup=types.ReplyKeyboardRemove()
    )


async def add_new_article(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Okay", reply_markup=types.ReplyKeyboardRemove()
    )

    
