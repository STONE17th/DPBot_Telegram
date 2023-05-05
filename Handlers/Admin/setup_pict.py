from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from Keyboards import kb_control
from loader import dp, bot, settings_db


class Posters(StatesGroup):
    start_poster = State()
    task_main = State()
    courses_my = State()
    courses_all = State()
    no_lecture = State()
    task_easy = State()
    task_normal = State()
    task_hard = State()
    settings = State()
    individual_courses = State()


@dp.message_handler(commands=['setup_pict'], state=None)
async def set_start_poster(message: Message):
    await bot.send_message(message.from_user.id, 'Начальная заставка: ', reply_markup=kb_control())
    await Posters.start_poster.set()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.start_poster)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'start_poster': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Задачи: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.task_main)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'task_main': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Мои курсы: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.courses_my)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'courses_my': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Все курсы: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.courses_all)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'courses_all': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Нет лекции: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.no_lecture)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'no_lecture': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Легкая задача: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.task_easy)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'task_easy': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Средняя задача: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.task_normal)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'task_normal': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Тяжелая задача: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.task_hard)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'task_hard': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Настройки: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.settings)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'settings': message.photo[0].file_id})
    await bot.send_message(message.from_user.id, 'Индивидуалочки: ', reply_markup=kb_control())
    await Posters.next()


@dp.message_handler(content_types=['photo', 'text'], state=Posters.individual_courses)
async def set_start_poster(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'individual_courses': message.photo[0].file_id})
    data = await state.get_data()
    for key, value in data.items():
        poster = ('poster', key, value, None, None, None)
        settings_db.set(poster)
    await state.reset_data()
    await state.finish()
    await bot.send_message(message.from_user.id, 'Заставки обновлены. Главное меню /start',
                           reply_markup=ReplyKeyboardRemove())
