from aiogram.types import Message, InputMediaPhoto
from aiogram.utils.exceptions import MessageCantBeEdited, MessageCantBeDeleted

from Classes import MyMessage, User
from Keyboards import ikb_start
from Keyboards.Callback import cb_menu
# from Misc import MsgToDict, PICTURES
from loader import dp, bot, users_db, settings_db
from temp import POSTERS, load_temp


@dp.callback_query_handler(cb_menu.filter(button='back'))
@dp.message_handler(commands=['start'])
async def start_command(_, user: User, msg: MyMessage):
    load_temp()
    poster = POSTERS.get('start_poster')
    caption = f'Привет, уважаемый {user.name}!'
    try:
        await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                     chat_id=msg.chat_id, message_id=msg.message_id,
                                     reply_markup=ikb_start(user.is_active_admin))
    except MessageCantBeEdited:
        await bot.send_photo(chat_id=msg.chat_id, photo=poster, caption=caption,
                             reply_markup=ikb_start(user.is_active_admin))


@dp.callback_query_handler(cb_menu.filter(button='message_delete'))
async def start_command(_, msg: MyMessage):
    try:
        await bot.delete_message(chat_id=msg.chat_id, message_id=msg.message_id)
    except MessageCantBeDeleted:
        pass
@dp.message_handler(commands=['start'])
async def cmd_start(message: Message, user: User):
    users_db.check(message.from_user.id)
    await message.answer(user.admin)
    # settings_db.set()
    # print(settings_db.load())

@dp.message_handler(content_types=['photo'])
async def experimental(message: Message):
    print(len(message.photo[0].file_id))


@dp.message_handler(commands=['add'])
async def cmd_add(message: Message):
    content = ('poster', 'start_poster', 'kjfskghkghdk', None, None, None)
    settings_db.set(content)
    # users_db.check(message.from_user.id)
    await message.answer('Загружено')


@dp.message_handler(commands=['purchase'])
async def cmd_add(message: Message):
    users_db.purchase(message.from_user.id, 'dp_basic_3')
    users_db.purchase(message.from_user.id, 'dp_basic_1:2')
    users_db.purchase(message.from_user.id, 'botboys_3')
    users_db.purchase(message.from_user.id, 'botboys_2:1')

@dp.message_handler(commands=['chat'])
async def cmd_add(message: Message):
    link = await bot.export_chat_invite_link(-971785765)
    await bot.send_message(message.from_user.id, link)


@dp.message_handler(commands=['chat_id'])
async def cmd_add(message: Message):
    print(message)