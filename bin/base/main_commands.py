from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    text = "Салют Я - твой помощник на канале Блока архитектора. " \
           "Я создан, чтобы улучшать контент, который выходит на канале, " \
           "создавать связь с подписчиками и в будущем, я буду помогать " \
           "ориентироваться в темах на канале."
    await message.answer(text)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    text = "Введите команду /start для начала работы."
    await message.answer(text)
