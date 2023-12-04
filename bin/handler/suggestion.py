from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from bin.ect import cfg
from bin.ect.utils import send_message
from bin.kb import inline
from bin.ect.model import Suggestions

router = Router()


class SuggestionState(StatesGroup):
    wait = State()


@router.callback_query(inline.Menu.filter(F.value == "Предложения"))
async def suggestion(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Если у вас есть предложения или пожелания по выпускаемому " \
           "контенту, оставьте его здесь! (темы для новых постов, " \
           "рубрик или оформления канала)"

    await state.set_state(SuggestionState.wait)

    await callback.message.edit_text(text)
    await callback.answer()


@router.message(SuggestionState.wait, F.text)
async def suggestion_message(message: Message, state: FSMContext) -> None:
    Suggestions.add(message.from_user.id, message.text)
    text_message = f"Пользователь {message.from_user.mention_html()} прислал сообщение:\n{message.text}"
    await send_message(cfg.ID_SENDER, text_message)

    await message.answer(cfg.BYE_MSG, reply_markup=inline.to_menu())
    await state.clear()
