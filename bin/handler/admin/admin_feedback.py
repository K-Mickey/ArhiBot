from aiogram.types import CallbackQuery
from aiogram import Router, F

from bin.kb import inline
from bin.ect.model import Feedbacks

router = Router()


@router.callback_query(inline.Admin.filter(F.value == "Отзывы"))
async def inline_feedbacks(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Отзывы", reply_markup=inline.admin_feedback())
    await callback.answer()


@router.callback_query(inline.Admin.filter(F.value == "Получить все отзывы"))
@router.callback_query(inline.Admin.filter(F.value == "Получить 5 отзывов"))
async def inline_get_all_feedbacks(callback: CallbackQuery) -> None:
    feedbacks = Feedbacks.get(5 if "Получить 5 отзывов" in callback.data else None)
    text = '' if feedbacks else "Нет отзывов"
    for feedback in feedbacks:
        text += f"<b>Отзыв от <a href='tg://user?id={feedback.user_id}'>{feedback.user_name}</a></b> {feedback.time}\n{feedback.text}\n\n"

    await callback.message.answer(text)
    from bin.handler.admin.admin import inline_admin
    await inline_admin(callback)
