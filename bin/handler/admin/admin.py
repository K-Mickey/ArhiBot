from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from bin.handler.admin import admin_feedback, admin_suggestion, admin_answer, admin_column, admin_question
from bin.kb import inline


router = Router()


@router.callback_query(inline.Menu.filter(F.value == "Админ"))
async def inline_admin(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer("Админ панель", reply_markup=inline.admin())
    await callback.answer()


async def message_admin(message: Message) -> None:
    await message.answer("Админ панель", reply_markup=inline.admin())


router.include_routers(
    admin_feedback.router,
    admin_suggestion.router,
    admin_answer.router,
    admin_column.router,
    admin_question.router
)
