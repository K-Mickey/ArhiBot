from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bin.ect import cfg
from bin.kb import inline
from bin.ect.model import Users

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    text = "<b>Салют!</b>\nЯ - твой помощник на канале - <a href='https://t.me/blockarchi'>Блока архитектора.</a>\n" \
           "<i>Я создан, чтобы улучшать контент, который выходит на канале, " \
           "создавать связь с подписчиками и в будущем, я буду помогать " \
           "ориентироваться в темах на канале.</i>\n\n" \
           "<b>Добро пожаловать!</b>😉"

    is_admin = True if str(message.from_user.id) in cfg.ID_ADMINS or \
                       str(message.chat.id) in cfg.ID_ADMINS else False
    await message.answer(text, reply_markup=inline.menu(is_admin))
    await state.clear()

    user = Users.get(message.from_user.id)
    if user is None:
        Users.add(message.from_user.id, message.from_user.full_name)
    elif user.name != message.from_user.full_name:
        Users.update(message.from_user.id, message.from_user.full_name)


@router.callback_query(inline.Menu.filter(F.value == "Меню"))
async def inline_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.answer()
    await start_command(callback.message, state)


@router.message(Command("about"))
async def about_command(message: Message) -> None:
    text = "По всем вопросам и предложениям разработки бота пишите " \
           "<a href='https://t.me/k_mickey'>создателю Михаилу.</a>"
    await message.answer(text)
