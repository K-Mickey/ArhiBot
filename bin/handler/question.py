from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bin.ect import cfg
from bin.ect.utils import send_message
from bin.kb import inline
from bin.ect.model import Questions, Answers, Columns
from bin.kb.inline import ColumnData

router = Router()


class QuestionState(StatesGroup):
    wait = State()


@router.callback_query(inline.Menu.filter(F.value == "Опросник"))
async def inline_menu(callback: CallbackQuery, state: FSMContext) -> None:
    text = "<b>Ответьте на небольшое количество вопросов о канале, " \
           "чтобы мы могли лучше понять запросы и ценности своей аудитории</b>"

    await callback.answer()
    await callback.message.delete()

    await state.set_state(QuestionState.wait)
    await callback.message.answer(text)
    await send_question(callback.message, state)


@router.callback_query(ColumnData.filter())
async def question_callback(callback: CallbackQuery, state: FSMContext, callback_data: ColumnData) -> None:
    await callback.answer()
    await callback.message.delete()
    column = Columns.get(int(callback_data.value))
    await update_data(column.text, state)
    await send_next_message(callback.message, state)


@router.message(QuestionState.wait, F.text)
async def send_question(message: Message, state: FSMContext) -> None:
    await update_data(message.text, state)
    await send_next_message(message, state)


async def update_data(text_answer: str, state: FSMContext) -> None:
    data = await state.get_data()

    # Если вопросы еще не заданы
    if "Вопросы" not in data:
        questions = Questions.get(only_visible=True)
        data["Вопросы"] = questions
        data["Ответы"] = {}
    questions = data["Вопросы"]

    # Проверка наличия предыдущего вопроса и сохранение
    if "Предыдущий" not in data:
        ind_next_question = 0
    else:
        data["Ответы"].update({questions[data["Предыдущий"]].question_id: text_answer})
        ind_next_question = data["Предыдущий"] + 1

    data["Предыдущий"] = ind_next_question
    await state.set_data(data)


async def send_next_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    questions = data["Вопросы"]
    ind_next_question = data.get("Предыдущий", 0)

    if ind_next_question < len(questions):
        next_question = questions[ind_next_question].text
    else:
        await last_question(message, state)
        return

    if cfg.COLUMN_KEY in next_question.lower():
        await message.answer(next_question, reply_markup=inline.column_custom())
    else:
        await message.answer(next_question)


async def last_question(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    answers = data["Ответы"]
    questions = data["Вопросы"]

    quiz = {}
    for question in questions:
        if answers[question.question_id] is None:
            continue
        quiz[question.text] = answers[question.question_id]
    quiz = "\n".join([f"{k}: {v}" for k, v in quiz.items()])

    Answers.add(message.from_user.id, answers)
    text_message = f"Пользователь {message.from_user.mention_html()} прислал сообщение:\n{quiz}"
    await send_message(cfg.ID_SENDER, text_message)

    await message.answer(cfg.BYE_MSG, reply_markup=inline.to_menu())
    await state.clear()
