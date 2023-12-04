from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F

from bin.kb import inline
from bin.ect.model import Columns

router = Router()


class AdminColumnState(StatesGroup):
    text = State()
    order = State()


class AdminColumnChangeState(StatesGroup):
    text = State()
    order = State()
    visible = State()


@router.callback_query(inline.Admin.filter(F.value == "Рубрики"))
async def inline_columns(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Рубрики", reply_markup=inline.admin_column())
    await callback.answer()


@router.callback_query(inline.Admin.filter(F.value == "Добавить рубрику"))
async def inline_add_column(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminColumnState.text)
    await callback.message.edit_text("Напишите название рубрики")
    await callback.answer()


@router.message(AdminColumnState.text)
async def message_add_column_text(message: Message, state: FSMContext) -> None:
    await state.set_state(AdminColumnState.order)
    await state.update_data(text=message.text)
    await message.answer("Напишите порядковый номер рубрики")


@router.message(AdminColumnState.order)
async def message_add_column_order(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    Columns.add(data["text"], int(message.text.strip()))
    await message.answer("Рубрика добавлена")
    await state.clear()
    from bin.handler.admin.admin import message_admin
    await message_admin(message)


@router.callback_query(inline.Admin.filter(F.value == "Изменить рубрики"))
async def inline_edit_column(callback: CallbackQuery) -> None:
    columns = Columns.get()

    text = "Выберите рубрику" if columns else "Нет рубрик"
    text_columns = {column.column_id: column.text for column in columns}
    await callback.message.answer(text, reply_markup=inline.admin_custom_column(text_columns))
    await callback.message.delete()
    await callback.answer()


@router.callback_query(inline.AdminButtonColumn.filter())
async def inline_edit_column_callback(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: inline.AdminButtonColumn
) -> None:
    await callback.answer()
    await callback.message.delete()
    column_id = int(callback_data.value)
    await state.update_data(column_id=column_id)
    await state.set_state(AdminColumnChangeState.text)

    button = Columns.get(column_id)

    await callback.message.answer(
        f"{button.text}\nПорядок: {button.order}\nВидимость: {'да' if button.visible else 'нет'}\n\n"
        f"Напишите новое название рубрики или отправьте '-'"
    )


@router.message(AdminColumnChangeState.text)
async def message_edit_column_text(message: Message, state: FSMContext) -> None:
    await state.set_state(AdminColumnChangeState.order)
    if message.text != "-":
        await state.update_data(text=message.text)
    await message.answer("Напишите порядковый номер рубрики или отправьте '-'")


@router.message(AdminColumnChangeState.order)
async def message_edit_column_order(message: Message, state: FSMContext) -> None:
    await state.set_state(AdminColumnChangeState.visible)
    if message.text != "-":
        await state.update_data(order=int(message.text.strip()))
    await message.answer("Напишите 'да', если включить видимость, 'нет' - выключить")


@router.message(AdminColumnChangeState.visible)
async def message_edit_column_visible(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    Columns.update(**data, visible=message.text.strip().lower() == "да")
    await message.answer("Рубрика изменена")
    await state.clear()
    from bin.handler.admin.admin import message_admin
    await message_admin(message)
