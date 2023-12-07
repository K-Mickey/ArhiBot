from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bin.ect.model import Columns


class Menu(CallbackData, prefix="menu"):
    value: str


class Admin(CallbackData, prefix="admin"):
    value: str


class AdminButtonColumn(CallbackData, prefix="admin_button"):
    value: str


class AdminButtonQuestion(CallbackData, prefix="admin_button_question"):
    value: int


class ColumnData(CallbackData, prefix="column_data"):
    value: str


def menu(is_admin: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Обратная связь", callback_data=Menu(value="Обратная связь"))
    builder.button(text="Предложения", callback_data=Menu(value="Предложения"))
    builder.button(text="Пройти опрос", callback_data=Menu(value="Пройти опрос"))

    if is_admin:
        builder.button(text="Админ", callback_data=Menu(value="Админ"))

    builder.adjust(1)
    return builder.as_markup()


def to_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Меню", callback_data=Menu(value="Меню"))
    builder.adjust(1)
    return builder.as_markup()


def admin() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Отзывы", callback_data=Admin(value="Отзывы"))
    builder.button(text="Предложения", callback_data=Admin(value="Предложения"))
    builder.button(text="Ответы", callback_data=Admin(value="Ответы"))
    builder.button(text="Рубрики", callback_data=Admin(value="Рубрики"))
    builder.button(text="Вопросы", callback_data=Admin(value="Вопросы"))
    builder.button(text="Меню", callback_data=Menu(value="Меню"))
    builder.adjust(1)
    return builder.as_markup()


def admin_question() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить вопрос", callback_data=Admin(value="Добавить вопрос"))
    builder.button(text="Изменить вопрос", callback_data=Admin(value="Изменить вопрос"))
    builder.button(text="Обратно", callback_data=Menu(value="Админ"))
    builder.adjust(1)
    return builder.as_markup()


def admin_column() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить рубрику", callback_data=Admin(value="Добавить рубрику"))
    builder.button(text="Изменить рубрики", callback_data=Admin(value="Изменить рубрики"))
    builder.button(text="Обратно", callback_data=Menu(value="Админ"))
    builder.adjust(1)
    return builder.as_markup()


def admin_answer() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить все ответы", callback_data=Admin(value="Получить все ответы"))
    builder.button(text="Получить 5 ответов", callback_data=Admin(value="Получить 5 ответов"))
    builder.button(text="Обратно", callback_data=Menu(value="Админ"))
    builder.adjust(1)
    return builder.as_markup()


def admin_feedback() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить все отзывы", callback_data=Admin(value="Получить все отзывы"))
    builder.button(text="Получить 5 отзывов", callback_data=Admin(value="Получить 5 отзывов"))
    builder.button(text="Обратно", callback_data=Menu(value="Админ"))
    builder.adjust(1)
    return builder.as_markup()


def admin_suggestion() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Получить все предложения", callback_data=Admin(value="Получить все предложения"))
    builder.button(text="Получить 5 предложений", callback_data=Admin(value="Получить 5 предложений"))
    builder.adjust(1)
    return builder.as_markup()


def admin_custom_column(buttons: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for column_id, text in buttons.items():
        builder.button(text=text, callback_data=AdminButtonColumn(value=str(column_id)))
    builder.button(text="Обратно", callback_data=Admin(value="Рубрики"))
    builder.adjust(1)
    return builder.as_markup()


def admin_custom_question(buttons: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for question_id, text in buttons.items():
        builder.button(text=text, callback_data=AdminButtonQuestion(value=question_id))
    builder.button(text="Обратно", callback_data=Admin(value="Вопросы"))
    builder.adjust(1)
    return builder.as_markup()


def column_custom() -> InlineKeyboardMarkup:
    columns = Columns.get()
    builder = InlineKeyboardBuilder()
    for column in columns:
        builder.button(text=column.text, callback_data=ColumnData(value=str(column.column_id)))
    builder.button(text="Завершить выбор", callback_data=ColumnData(value="Завершить выбор"))
    builder.adjust(1)
    return builder.as_markup()
