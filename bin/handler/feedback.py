from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from bin.ect import cfg
from bin.ect.utils import send_message
from bin.kb import inline
from bin.ect.model import Feedbacks

router = Router()


class FeedbackState(StatesGroup):
    wait = State()


@router.callback_query(inline.Menu.filter(F.value == "Обратная связь"))
async def feedback(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Оставьте обратную связь о нашем канале и " \
           "помогите нам стать лучше - ваше мнение ценно!"

    await state.set_state(FeedbackState.wait)

    await callback.message.edit_text(text)
    await callback.answer()


@router.message(FeedbackState.wait, F.text)
async def feedback_message(message: Message, state: FSMContext) -> None:
    text = "Большое спасибо за ваше внимание и ответ! " \
           "Если вы хотите продолжить взаимодействие, " \
           "нажимайте на меню внизу"

    Feedbacks.add(message.from_user.id, message.text)
    text_message = f"Пользователь {message.from_user.mention_html()} " \
                   f"прислал сообщение:\n{message.text}"
    await send_message(cfg.ID_SENDER, text_message)

    await message.answer(text, reply_markup=inline.to_menu())
    await state.clear()
