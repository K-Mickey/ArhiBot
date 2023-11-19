from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bin.kb import inline


router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    text = "Салют\nЯ - твой помощник на канале Блока архитектора.\n" \
           "Я создан, чтобы улучшать контент, который выходит на канале, " \
           "создавать связь с подписчиками и в будущем, я буду помогать " \
           "ориентироваться в темах на канале."
    await message.answer(text, reply_markup=inline.menu())


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    text = "Введите команду /start для начала работы."
    await message.answer(text)
