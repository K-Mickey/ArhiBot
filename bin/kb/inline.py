from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Menu(CallbackData, prefix="menu"):
    value: str


def menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Обратная связь", callback_data=Menu(value="Обратная связь"))
    builder.button(text="Предложения", callback_data=Menu(value="Предложения"))
    builder.button(text="Опросник", callback_data=Menu(value="Опросник"))
    builder.adjust(1)
    return builder.as_markup()


def to_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Меню", callback_data=Menu(value="Меню"))
    builder.adjust(1)
    return builder.as_markup()
