from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto

from Keyboards import ikb_confirm, ikb_notification
from Keyboards.Callback import cb_menu
from Keyboards import kb_control, kb_stream
from Classes import MyMessage, User
from loader import dp, bot, settings_db
from temp import POSTERS
from Misc import user_notify


class Stream(StatesGroup):
    name = State()
    date_time = State()
    desc = State()
    poster = State()
    url = State()
    confirm = State()


class News(StatesGroup):
    name = State()
    desc = State()
    poster = State()
    url = State()
    confirm = State()

@dp.callback_query_handler(cb_menu.filter(button='notification'))
async def notification_menu(_, msg: MyMessage, user: User):
    poster = POSTERS.get('no_lecture')
    caption = 'Выбери тип оповещения: Новость или стрим'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id,
                                 message_id=msg.message_id,
                                 reply_markup=ikb_notification())


@dp.callback_query_handler(cb_menu.filter(button='stream'), state=None)
async def create_stream(_, msg: MyMessage, user: User):
    await bot.send_message(user.id, 'Введите название стрима:', reply_markup=kb_control())
    await Stream.name.set()


@dp.message_handler(state=Stream.name)
async def stream_name(message: Message, user: User, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(text='Введите дату и время:', reply_markup=kb_control())
    await Stream.next()


@dp.message_handler(state=Stream.date_time)
async def stream_date(message: Message, state: FSMContext):
    await state.update_data({'date_time': message.text})
    await message.answer(text='Введите описание:', reply_markup=kb_control())
    await Stream.next()


@dp.message_handler(state=Stream.desc)
async def stream_poster(message: Message, state: FSMContext):
    await state.update_data({'desc': message.text})
    await message.answer(text='Введите обложку для стрима:', reply_markup=kb_control())
    await Stream.next()


@dp.message_handler(content_types='photo', state=Stream.poster)
async def stream_url(message: Message, state: FSMContext):
    await state.update_data({'poster': message.photo[0].file_id})
    await message.answer(text='Введите площадку для стрима:', reply_markup=kb_stream())
    await Stream.next()


@dp.message_handler(state=Stream.url)
async def stream_confirm(message: Message, state: FSMContext):
    stream_url = settings_db.select_url(message.text)
    await state.update_data({'url': stream_url if stream_url else message.text})
    data = await state.get_data()
    caption = f"Название: {data.get('name')}\n{data.get('data_time')}\n\n{data.get('desc')}\n\n{data.get('url')}"
    await bot.send_photo(chat_id=message.from_user.id, photo=data.get('poster'), caption=caption,
                         reply_markup=ikb_confirm('stream', 'confirm'))
    await Stream.next()


@dp.callback_query_handler(state=Stream.confirm)
async def stream_send(call: CallbackQuery, msg: MyMessage, state: FSMContext):
    if msg.confirm:
        data = await state.get_data()
        caption = (f'{data.get("name")}\n{data.get("data_time")}\n\n{data.get("desc")}', data.get('poster'))
        await user_notify('stream', caption, data.get('url'))
        await call.answer(f'Стрим {data.get("name")} анонсирован!', show_alert=True)
    else:
        await call.answer('Отмена')
    await bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)
    await bot.send_message(msg.chat_id, text='Вернуться в главное меню /start')
    await state.reset_data()
    await state.finish()


@dp.callback_query_handler(cb_menu.filter(button='news'), state=None)
async def create_news(_, msg: MyMessage, user: User):
    await bot.send_message(user.id, 'Введите тему новости:', reply_markup=kb_control())
    await News.name.set()


@dp.message_handler(state=News.name)
async def stream_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(text='Введите саму новость:', reply_markup=kb_control())
    await News.next()


@dp.message_handler(state=News.desc)
async def stream_date(message: Message, state: FSMContext):
    await state.update_data({'desc': message.text})
    await message.answer(text='Картинка для новости:', reply_markup=kb_control())
    await News.next()


@dp.message_handler(content_types='photo', state=News.poster)
async def stream_url(message: Message, state: FSMContext):
    await state.update_data({'poster': message.photo[0].file_id})
    await message.answer(text='Введите ссылку новости:', reply_markup=kb_control())
    await News.next()


@dp.message_handler(state=News.url)
async def stream_confirm(message: Message, state: FSMContext):
    await state.update_data({'url': message.text})
    data = await state.get_data()
    caption = f"Тема: {data.get('name')}\n\n{data.get('desc')}\n\n{data.get('url')}"
    await bot.send_photo(chat_id=message.from_user.id, photo=data.get('poster'), caption=caption,
                         reply_markup=ikb_confirm('stream', 'confirm'))
    await News.next()


@dp.callback_query_handler(state=News.confirm)
async def stream_send(call: CallbackQuery, msg: MyMessage, state: FSMContext):
    if msg.confirm:
        data = await state.get_data()
        url: str = data.get('url')
        caption = f"Тема: {data.get('name')}\n\n{data.get('desc')}\n\n" + (url if url.startswith('http') else '')
        poster = data.get('poster')
        message = (caption, poster)
        await user_notify('news', message)
        await call.answer(f'Новость {data.get("name")} разослана!', show_alert=True)
    else:
        await call.answer('Отмена')
    await bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)
    await bot.send_message(msg.chat_id, text='Вернуться в главное меню /start')
    await state.reset_data()
    await state.finish()


@dp.callback_query_handler(cb_menu.filter(button='pin_news'))
async def pin_news(_, msg: MyMessage):
    await bot.pin_chat_message(chat_id=msg.chat_id, message_id=msg.message_id)
