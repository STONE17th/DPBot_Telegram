from aiogram.types import Message, InputMediaPhoto, CallbackQuery
from aiogram.utils.exceptions import MessageCantBeEdited, MessageCantBeDeleted

from Classes import MyMessage, User, Course, Lecture
from Keyboards import ikb_start, ikb_confirm
from Keyboards.Callback import cb_menu, confirm
# from Misc import MsgToDict, PICTURES
from loader import dp, bot, users_db, courses_db, settings_db
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
    prod = 'new_table'
    my_prod = [prod.split(':')[0], int(prod.split(':')[1])] if ':' in prod else [prod]
    my_product = courses_db.my_purchase(*my_prod)
    print(my_product)
    my_product = Lecture(my_product, my_prod[0]) if ':' in prod else Course(my_product)
    print(my_product.poster)
    # poster = my_product[4]
    # content = ('poster', 'start_poster', 'kjfskghkghdk', None, None, None)
    # settings_db.set(content)
    # # users_db.check(message.from_user.id)
    # await message.answer('Загружено')




@dp.message_handler(commands=['im_admin'])
async def new_admin(message: Message, user: User):
    mention = "[" + user.name + "](tg://user?id=" + str(user.id) + ")"
    await bot.send_message(409205647, text=f'{mention} хочет стать админом',
                           parse_mode='markdown',
                           reply_markup=ikb_confirm('new_admin', user.id))


@dp.callback_query_handler(confirm.filter(menu='new_admin'))
async def confirm_admin(call: CallbackQuery, msg: MyMessage, user: User):
    if msg.confirm:
        users_db.set_admin(int(msg.args))
        await call.answer('Новый админ!', show_alert=True)
        await bot.send_message(int(msg.args), text='Теперь ты админ')
    else:
        await bot.send_message(int(msg.args), text='Тебе отказано')
