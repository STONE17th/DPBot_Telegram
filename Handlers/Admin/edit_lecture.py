from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from Classes import MyMessage, User
from Keyboards import ikb_confirm, kb_control
from Keyboards.Callback import course_navigation
from loader import dp, bot, courses_db
from Misc import user_notify

KEYS = ('id', 'name', 'description', 'poster', 'lect_url', 'semi_url', 'comp_url', 'date', 'price', 'finished')
class Lecture(StatesGroup):
    name = State()
    description = State()
    poster = State()
    lect_url = State()
    semi_url = State()
    comp_url = State()
    date = State()
    price = State()
    confirm = State()


@dp.callback_query_handler(course_navigation.filter(menu='edit_lecture'), state=None)
async def new_lecture_catch(_, msg: MyMessage, user: User, state: FSMContext):
    await state.update_data({'table_name': msg.table})
    await state.update_data({'id': msg.id})
    await bot.send_message(user.id, 'Введите название лекции:', reply_markup=kb_control())
    await Lecture.name.set()


@dp.message_handler(state=Lecture.name)
async def desc_catch(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'name': message.text})
    await message.answer(text='Введите описание лекции:', reply_markup=kb_control())
    await Lecture.next()


@dp.message_handler(state=Lecture.description)
async def poster_catch(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'description': message.text})
    await message.answer(text='Загрузите обложку лекции:', reply_markup=kb_control())
    await Lecture.next()


@dp.message_handler(content_types=['photo', 'text'], state=Lecture.poster)
async def video_catch(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'poster': message.photo[0].file_id})
    await message.answer(text='Введите ссылку на лекцию:', reply_markup=kb_control())
    await Lecture.next()


@dp.message_handler(state=Lecture.lect_url)
async def compendium_catch(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'lect_url': message.text})
    await message.answer(text='Введите ссылку на семинар:', reply_markup=kb_control())
    await Lecture.next()


@dp.message_handler(state=Lecture.semi_url)
async def price_catch(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'semi_url': message.text})
    await message.answer(text='Введите ссылку на конспект:', reply_markup=kb_control())
    await Lecture.next()


@dp.message_handler(state=Lecture.comp_url)
async def price_catch(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'comp_url': message.text})
    await message.answer(text='Введите дату начала лекции:', reply_markup=kb_control())
    await Lecture.next()


@dp.message_handler(state=Lecture.date)
async def price_catch(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'date': message.text})
    await message.answer(text='Введите цену лекции:', reply_markup=kb_control())
    await Lecture.next()


@dp.message_handler(state=Lecture.price)
async def confirm_catch(message: Message, state: FSMContext, msg: MyMessage):
    if message.text != 'Дальше':
        await state.update_data({'price': message.text})
    data = await state.get_data()
    caption = f"Название: {data.get('name')}\nОписание: {data.get('description')}\n\n" \
              f"Ссылка на видео: {data.get('lect_url')}\nСсылка на семинар: {data.get('semi_url')}" \
              f"\nСсылка на конспект: {data.get('comp_url')}\n\nДата лекции: {data.get('date')}\n\nЦена курса: {data.get('price')}"
    if data.get('poster'):
        await bot.send_photo(chat_id=msg.chat_id, photo=data.get('poster'), caption=caption,
                             reply_markup=ikb_confirm('class', 'confirm'))
    else:
        await bot.send_message(chat_id=msg.chat_id, text=caption, reply_markup=ikb_confirm('class', 'confirm'))
    await Lecture.next()


@dp.callback_query_handler(state=Lecture.confirm)
async def save_lecture(call: CallbackQuery, state: FSMContext, msg: MyMessage):
    if msg.confirm:
        data = await state.get_data()
        table_name, index = data.get('table_name'), data.get('id')
        cur_lecture = {item[0]: item[1] for item in zip(KEYS, courses_db.lecture(table_name, False, index))}
        cur_lecture.update(data)
        upd_lect = tuple([value for key, value in cur_lecture.items() if key not in ['id', 'table_name', 'finished']])
        try:
            courses_db.update(upd_lect, table_name, index)
            await call.answer(f'Лекция {data.get("name")} внесена в БД', show_alert=True)
        except:
            await call.answer('Ошибка при добавлении лекции', show_alert=True)
        poster = cur_lecture.get('poster')
        text = f'В курс {courses_db.name(table_name)} добавлена {index} лекция\n{data.get("name")}'
        await user_notify('courses', (poster, text), table_name)
    #     name = course_db.select(data.get('table'))[1]
    #     caption = f'Курс: {name}\nПоявился доступ к лекции "{data.get("name")}"'
    #     message = (caption, data.get('poster'))
    #     await user_distribution('courses', message, data.get('table'))
    # else:
    #     await call.answer('Отмена')
    # await bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)
    # await bot.send_message(msg.my_id, text='Вернуться в главное меню /start')
    await state.reset_data()
    await state.finish()
