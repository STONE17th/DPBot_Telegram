from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from Classes import MyMessage
from Keyboards import kb_control, ikb_confirm, ikb_main
from Keyboards.Callback import cb_menu
from Misc import user_notify
from loader import dp, bot, courses_db
from temp import POSTERS


class NewCourse(StatesGroup):
    table_name = State()
    name = State()
    description = State()
    poster = State()
    lect_semi = State()
    start_date = State()
    price = State()
    confirm = State()


@dp.callback_query_handler(cb_menu.filter(button='new_course'), state=None)
async def enter_table(message: Message):
    await bot.send_message(message.from_user.id, 'Введите название таблицы:', reply_markup=kb_control('cancel'))
    await NewCourse.table_name.set()


@dp.message_handler(state=NewCourse.table_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data({'table_name': message.text})
    await message.answer('Введите название курса:', reply_markup=kb_control('cancel'))
    await NewCourse.next()


@dp.message_handler(state=NewCourse.name)
async def enter_description(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(text='Введите описание курса:', reply_markup=kb_control('cancel'))
    await NewCourse.next()


@dp.message_handler(state=NewCourse.description)
async def enter_poster(message: Message, state: FSMContext):
    await state.update_data({'description': message.text})
    await message.answer(text='Введите обложку курса:', reply_markup=kb_control('cancel'))
    await NewCourse.next()


@dp.message_handler(content_types='photo', state=NewCourse.poster)
async def enter_tg_url(message: Message, state: FSMContext):
    await state.update_data({'poster': message.photo[0].file_id})
    await message.answer(text='Введите количество лекций и семинаров:', reply_markup=kb_control('cancel'))
    await NewCourse.next()


@dp.message_handler(state=NewCourse.lect_semi)
async def enter_date(message: Message, state: FSMContext):
    await state.update_data({'lect_semi': message.text})
    await message.answer(text='Введите дату начала курса:', reply_markup=kb_control('date'))
    await NewCourse.next()


@dp.message_handler(state=NewCourse.start_date)
async def enter_price(message: Message, state: FSMContext):
    await state.update_data({'start_date': message.text})
    await message.answer(text='Введите полную стоимость курса:', reply_markup=kb_control('cancel'))
    await NewCourse.next()


@dp.message_handler(state=NewCourse.price)
async def confirm_new_course(message: Message, state: FSMContext):
    await state.update_data({'price': int(message.text)})
    data = await state.get_data()
    caption = f"Название: {data.get('name')} ({data.get('table_name')})\n\nПродолжительность: " \
              f"{data.get('lect_semi').split(':')[0]} лекций и {data.get('lect_semi').split(':')[1]} семинаров\n\n" \
              f"Описание: {data.get('description')}\n\nЦена курса: {data.get('price')}\n\n" \
              f"Дата начала: {data.get('start_date')}"
    await bot.send_photo(chat_id=message.from_user.id, photo=data.get('poster'), caption=caption,
                         reply_markup=ikb_confirm('course', 'confirm'))
    await NewCourse.next()


@dp.callback_query_handler(state=NewCourse.confirm)
async def save_new_course(call: CallbackQuery, msg: MyMessage, state: FSMContext):
    if msg.confirm:
        data = await state.get_data()
        caption = f'Курс {data.get("name")} добавлен в список Dirty Python Bot'
        poster = data.get('poster')
        message = (poster, caption)
        try:
            courses_db.add(data)
            await user_notify('courses', message)
            await user_notify('news', message)
        except:
            poster = POSTERS.get('cancel')
            caption = 'Ошибка добавления в базу!'
    else:
        poster = POSTERS.get('cancel')
        caption = 'ОТМЕНА!'
    await state.reset_data()
    await state.finish()
    await bot.send_photo(call.message.chat.id, photo=poster, caption=caption,
                         reply_markup=ikb_main())
