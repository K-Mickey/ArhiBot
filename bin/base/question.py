from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from bin.db.db import get_questions, add_answers
from bin.ect import cfg
from bin.ect.utils import send_message
from bin.kb import inline

router = Router()


class QuestionState(StatesGroup):
    wait = State()


@router.callback_query(inline.Menu.filter(F.value == "Опросник"))
async def inline_menu(callback: CallbackQuery, state: FSMContext) -> None:
    text = "Ответьте на небольшое количество вопросов о канале, " \
           "чтобы мы могли лучше понять запросы и ценности своей аудитории:"

    await state.set_state(QuestionState.wait)

    await callback.answer()
    await callback.message.edit_text(text)


@router.callback_query(QuestionState.wait, F.text)
async def question_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await send_question(callback.message, state)


@router.message(QuestionState.wait, F.text)
async def send_question(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    if "Вопросы" not in data:
        data["Вопросы"] = get_questions()
    questions = data["Вопросы"]

    if "Предыдущий" not in data and questions:
        ind_next_question = 0
    else:
        await state.set_data({"Ответы": {
            questions[data["Предыдущий"]].question_id: message.text
        }})
        ind_next_question = data["Предыдущий"] + 1

    if ind_next_question < len(questions):
        next_question = questions[ind_next_question].text
    else:
        await last_question(message, state)
        return

    await state.set_data({"Предыдущий": ind_next_question})
    await message.answer(next_question)


async def last_question(message: Message, state: FSMContext) -> None:
    text = "Большое спасибо за ваше внимание и ответ! " \
           "Если вы хотите продолжить взаимодействие, " \
           "нажимайте на меню внизу"

    data = await state.get_data()
    answers = data["Ответы"]
    questions = data["Вопросы"]

    quiz = {}
    for question in questions:
        if answers[question.question_id] is None:
            continue
        quiz[question.text] = answers[question.question_id]
    quiz = "\n".join([f"{k}: {v}" for k, v in quiz.items()])

    add_answers(message.from_user.id, answers)
    text_message = f"Пользователь {message.from_user.get_mention()} " \
                   f"прислал сообщение:\n{quiz}"
    await send_message(cfg.ID_SENDER, text_message)

    await message.answer(text, reply_markup=inline.to_menu())
    await state.clear()
