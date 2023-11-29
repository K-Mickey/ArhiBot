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

    if not answers:
        await callback.message.answer("Нет ответов")
    else:
        answers_text = {}
        for answer in answers:
            sep = (answer.user_name, answer.time)
            if sep not in answers_text:
                answers_text[sep] = \
                    f"<b>Ответы от <a href='tg://user?id={answer.user_id}'>{answer.user_name}</a></b> {answer.time}"

            answers_text[sep] += f"\n\nНа вопрос: {answer.question_text}\n{answer.text}"
        for text in answers_text.values():
            await callback.message.answer(text)
    from bin.handler.admin.admin import inline_admin
    await inline_admin(callback)
