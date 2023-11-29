from aiogram import Router, F
from aiogram.types import CallbackQuery

from bin.kb import inline
from bin.ect.model import Suggestions

router = Router()


@router.callback_query(inline.Admin.filter(F.value == "Предложения"))
async def inline_suggestion(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Предложения", reply_markup=inline.admin_suggestion())
    await callback.answer()


@router.callback_query(inline.Admin.filter(F.value == "Получить все предложения"))
@router.callback_query(inline.Admin.filter(F.value == "Получить 5 предложений"))
async def inline_get_all_suggestions(callback: CallbackQuery) -> None:
    suggestions = Suggestions.get(5 if "Получить 5 предложений" in callback.data else None)

    text = '' if suggestions else "Нет предложений"
    for suggestion in suggestions:
        text += f'<b>Предложение от {suggestion.name}</b> {suggestion.time}\n{suggestion.text}\n\n'
    await callback.message.answer(text)
    from bin.handler.admin.admin import inline_admin
    await inline_admin(callback)
