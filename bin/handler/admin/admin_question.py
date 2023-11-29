from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from bin.kb import inline
from bin.kb.inline import AdminButtonQuestion
from bin.ect.model import Questions

router = Router()


class AdminQuestionAddState(StatesGroup):
    text = State()
    order = State()


class AdminQuestionUpdateState(StatesGroup):
    text = State()
    order = State()
    visible = State()


@router.callback_query(inline.Admin.filter(F.value == "Вопросы"))
async def inline_questions(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Вопросы", reply_markup=inline.admin_question())
    await callback.answer()


"""
Добавление новых вопросов
"""


@router.callback_query(inline.Admin.filter(F.value == "Добавить вопрос"))
async def inline_add_question(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminQuestionAddState.text)
    await callback.message.edit_text("Напишите вопрос")
    await callback.answer()


@router.message(AdminQuestionAddState.text)
async def message_add_question_text(message: Message, state: FSMContext) -> None:
    await state.set_state(AdminQuestionAddState.order)
    await state.update_data(text=message.text)
    await message.answer("Напишите порядковый номер вопроса")


@router.message(AdminQuestionAddState.order)
async def message_add_question_order(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    Questions.add(data["text"], int(message.text.strip()))
    await message.answer("Вопрос добавлен")
    await state.clear()
    from bin.handler.admin.admin import message_admin
    await message_admin(message)


"""
Изменение существующих вопросов
"""


@router.callback_query(inline.Admin.filter(F.value == "Изменить вопрос"))
async def inline_edit_question(callback: CallbackQuery, state: FSMContext) -> None:
    questions = Questions.get()

    text = "Выберите вопрос" if questions else "Нет вопросов"
    buttons_questions = {question.question_id: question.text for question in questions}
    await callback.message.answer(text, reply_markup=inline.admin_custom_question(buttons_questions))
    await callback.answer()


@router.callback_query(inline.AdminButtonQuestion.filter())
async def inline_edit_question_callback(callback: CallbackQuery, state: FSMContext,
                                        callback_data: AdminButtonQuestion) -> None:
    await state.set_state(AdminQuestionUpdateState.text)
    question_id = int(callback_data.value)
    question = Questions.get(question_id)
    await callback.message.edit_text(
        f"{question.text}\nПорядок: {question.order}\nВидимость: {'да' if question.visible else 'нет'}"
        f"\n\nНапишите новый вопрос или отправьте '-' "
    )
    await callback.answer()
    await state.update_data({'question_id': question_id})


@router.message(AdminQuestionUpdateState.text)
async def message_edit_question_text(message: Message, state: FSMContext) -> None:
    await state.set_state(AdminQuestionUpdateState.order)
    if message.text != '-':
        await state.update_data(text=message.text)
    await message.answer("Напишите порядковый номер вопроса или отправьте '-' ")


@router.message(AdminQuestionUpdateState.order)
async def message_edit_question_order(message: Message, state: FSMContext) -> None:
    await state.set_state(AdminQuestionUpdateState.visible)
    if message.text != '-':
        await state.update_data(order=int(message.text))
    await message.answer("Напишите 'да', если включить видимость, 'нет' - выключить")


@router.message(AdminQuestionUpdateState.visible)
async def message_edit_question_visible(message: Message, state: FSMContext) -> None:
    await state.update_data(visible=message.text.strip().lower() == 'да')
    data = await state.get_data()
    Questions.update(**data)
    await message.answer("Вопрос изменен")
    await state.clear()
    from bin.handler.admin.admin import message_admin
    await message_admin(message)
