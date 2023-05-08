from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from Classes import MyMessage
from Keyboards import kb_control
from Keyboards.Callback import cb_menu
from loader import dp, bot, settings_db


class Links(StatesGroup):
    you_tube = State()
    zoom = State()
    main_telegram = State()
    boosty = State()
    donation = State()
    owner = State()
    admin = State()


@dp.callback_query_handler(cb_menu.filter(button='setup_links'), state=None)
# @dp.message_handler(commands=['setup_links'], state=None)
async def set_you_tube(_, msg: MyMessage):
    await bot.send_message(msg.message_id, 'Ссылка на YouTube канал: : ', reply_markup=kb_control())
    await Links.you_tube.set()


@dp.message_handler(content_types=['text'], state=Links.you_tube)
async def set_zoom(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'you_tube': message.text})
    await bot.send_message(message.from_user.id, 'Ссылка на ZOOM: ', reply_markup=kb_control())
    await Links.next()


@dp.message_handler(content_types=['text'], state=Links.zoom)
async def set_telegram(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'zoom': message.text})
    await bot.send_message(message.from_user.id, 'Ссылка на Telegram: ', reply_markup=kb_control())
    await Links.next()


@dp.message_handler(content_types=['text'], state=Links.main_telegram)
async def set_boosty(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'main_telegram': message.text})
    await bot.send_message(message.from_user.id, 'Ссылка на Boosty: ', reply_markup=kb_control())
    await Links.next()


@dp.message_handler(content_types=['text'], state=Links.boosty)
async def set_donation(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'boosty': message.text})
    await bot.send_message(message.from_user.id, 'Ссылка на DonationAlerts: ', reply_markup=kb_control())
    await Links.next()


@dp.message_handler(content_types=['text'], state=Links.donation)
async def set_owner(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'donation': message.text})
    await bot.send_message(message.from_user.id, 'Ссылка на владельца: ', reply_markup=kb_control())
    await Links.next()


@dp.message_handler(content_types=['text'], state=Links.owner)
async def set_admin(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'owner': message.text})
    await bot.send_message(message.from_user.id, 'Ссылка на админа: ', reply_markup=kb_control())
    await Links.next()


@dp.message_handler(content_types=['text'], state=Links.admin)
async def save_links(message: Message, state: FSMContext):
    if message.text != 'Дальше':
        await state.update_data({'admin': message.text})
    data = await state.get_data()
    settings_db.save_settings(data, 'link')
    await state.reset_data()
    await state.finish()
    await bot.send_message(message.from_user.id, 'Ссылки обновлены. Главное меню /start',
                           reply_markup=ReplyKeyboardRemove())
