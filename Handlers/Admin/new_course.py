# from Keyboards.Callback import main_menu
# from Misc import user_distribution
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from Classes import MyMessage
from Keyboards import kb_control, ikb_confirm
from Keyboards.Callback import cb_menu
from loader import dp, bot, courses_db
from Misc import user_notify


# from ..start import cmd_start


class NewCourse(StatesGroup):
    table = State()
    name = State()
    description = State()
    poster = State()
    tg_url = State()
    disc_url = State()
    quantity = State()
    start_date = State()
    price = State()
    course_confirm = State()


# @dp.message_handler(commands=['add_course'])
@dp.callback_query_handler(cb_menu.filter(button='new_course'), state=None)
async def enter_table(message: Message):
    await bot.send_message(message.from_user.id, 'Введите название таблицы:', reply_markup=kb_control())
    await NewCourse.table.set()


@dp.message_handler(state=NewCourse.table)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data({'table_name': message.text})
    await message.answer('Введите название курса:', reply_markup=kb_control())
    await NewCourse.next()


@dp.message_handler(state=NewCourse.name)
async def enter_description(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(text='Введите описание курса:', reply_markup=kb_control())
    await NewCourse.next()


@dp.message_handler(state=NewCourse.description)
async def enter_poster(message: Message, state: FSMContext):
    await state.update_data({'description': message.text})
    await message.answer(text='Введите обложку курса:', reply_markup=kb_control())
    await NewCourse.next()


@dp.message_handler(content_types='photo', state=NewCourse.poster)
async def enter_tg_url(message: Message, state: FSMContext):
    await state.update_data({'poster': message.photo[0].file_id})
    await message.answer(text='Введите яндекс-облако курса:', reply_markup=kb_control())
    await NewCourse.next()


@dp.message_handler(state=NewCourse.disc_url)
async def enter_quantity(message: Message, state: FSMContext):
    await state.update_data({'disc_url': message.text})
    await message.answer(text='Введите количество лекций:', reply_markup=kb_control())
    await NewCourse.next()


@dp.message_handler(state=NewCourse.quantity)
async def enter_date(message: Message, state: FSMContext):
    await state.update_data({'quantity': int(message.text)})
    await message.answer(text='Введите дату начала курса:', reply_markup=kb_control())
    await NewCourse.next()


@dp.message_handler(state=NewCourse.start_date)
async def enter_price(message: Message, state: FSMContext):
    await state.update_data({'start_date': message.text})
    await message.answer(text='Введите полную стоимость курса:', reply_markup=kb_control())
    await NewCourse.next()


@dp.message_handler(state=NewCourse.price)
async def confirm_new_course(message: Message, state: FSMContext):
    await state.update_data({'price': message.text})
    data = await state.get_data()
    caption = f"Название: {data.get('name')}\n\nНазвание таблицы: {data.get('table_name')}\n\n" \
              f"Продолжительность: {data.get('quantity')} лекций\n\n" \
              f"Описание: {data.get('description')}\n\nРабочая папка: {data.get('disc_url')}\n" \
              f"\n\nЦена курса: {data.get('price')}\n\nДата начала: {data.get('start_date')}"
    await bot.send_photo(chat_id=message.from_user.id, photo=data.get('poster'), caption=caption,
                         reply_markup=ikb_confirm('course', 'confirm'))
    await NewCourse.next()


@dp.callback_query_handler(state=NewCourse.course_confirm)
async def save_new_course(call: CallbackQuery, msg: MyMessage, state: FSMContext):
    if msg.confirm:
        data = await state.get_data()
        courses_db.add(data)
        await call.answer(f'Курс {data.get("name")} добавлен в БД')
        caption = f'Курс {data.get("name")} добавлен в список Dirty Python Bot'
        poster = data.get('poster')
        message = (poster, caption, )
        await user_notify('courses', message)
        await user_notify('news', message)
    else:
        await call.answer('Отмена')
    await state.reset_data()
    await state.finish()
    await bot.send_message(call.message.chat.id, text='Вернуться в главное меню /start')
    # await cmd_start(message)
