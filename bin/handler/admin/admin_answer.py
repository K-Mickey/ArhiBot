from aiogram import Router, F
from aiogram.types import CallbackQuery

from bin.kb import inline
from bin.ect.model import Answers

router = Router()


@router.callback_query(inline.Admin.filter(F.value == "Ответы"))
async def inline_answer(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Ответы", reply_markup=inline.admin_answer())
    await callback.answer()


@router.callback_query(inline.Admin.filter(F.value == "Получить все ответы"))
@router.callback_query(inline.Admin.filter(F.value == "Получить 5 ответов"))
async def inline_get_all_answers(callback: CallbackQuery) -> None:
    answers = Answers.get(5 if "Получить 5 ответов" in callback.data else None)

    text = '' if answers else "Нет ответов"
    for answer in answers:
        text += f'<b>Ответ от {answer.user_id}</b> {answer.time}\nНа вопрос: {answer.question_id}\n{answer.text}\n\n'
    await callback.message.answer(text)
    from bin.handler.admin.admin import inline_admin
    await inline_admin(callback)
