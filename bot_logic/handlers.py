from aiogram import Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from bot_logic.ai_roles import ROLES
from bot_logic.ai_tool import get_gigachat_response
from bot_logic.callback_data import RoleSelect

handlers_router = Router()

@handlers_router.message(Command(commands=["start"])) #если на роутер пришло сообщение, которое содержит старт, то будет вызвана функция ниже
async def start_handler(message: Message):
    await message.answer(text="Привет!\n\nЯ бот для важных переговоров!\n\nПросто отправь мне свой текст)")


@handlers_router.callback_query(RoleSelect.filter())
async def ai_handler(query: CallbackQuery, callback_data: RoleSelect, state: FSMContext):
    user_text = await state.get_value("user_text")

    ai_response = await get_gigachat_response(user_text=user_text, role=callback_data.role)

    await query.message.edit_text(text=ai_response, reply_markup=None)

# state - машина состояний. когда пользователь напишет смс, мы его сохраняем в state, а пользователю выдаем список кнопок.
# пользователь нажимает на кнопку, попадает во 2й обработчик. там из state берем смс пользователя и отравляем в гигачат
# а пользователю возвращаем ответ
@handlers_router.message()
async def role_handler(message: Message, state: FSMContext):
    await state.update_data(user_text=message.text)

    keyboard = [
        [
            InlineKeyboardButton(
                text=value.get("name"),
                callback_data=RoleSelect(role=key).pack(),
                style=value.get("style")
            )
        ]
    for key, value in ROLES.items()
    ]

    await message.answer(
        text="В каком стиле хочешь получить ответ?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
