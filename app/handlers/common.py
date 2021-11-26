from aiogram import dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


def register_handlers_common(dp: dispatcher, ):
    dp.register_message_handler(greeting, commands=["start", "help", "restart"], state="*")


async def greeting(message: types.message, state: FSMContext) -> str:
    await state.finish()
    await message.answer(
        "I'm ARticleBot!\nPowered by aiogram.\nI'll help u storage and categorize your articles",
        parse_mode=types.ParseMode.HTML,
    )
