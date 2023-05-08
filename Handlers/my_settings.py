from aiogram.types import InputMediaPhoto

from Classes import MyMessage, User
from Keyboards import ikb_settings, ikb_links
from Keyboards.Callback import cb_menu
from loader import dp, bot, users_db
from temp import POSTERS


@dp.callback_query_handler(cb_menu.filter(button='my_settings'))
async def my_settings(_, msg: MyMessage, user: User):
    poster = POSTERS.get('settings')
    caption = f'{user.name}, это твои настройки'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id,
                                 message_id=msg.message_id,
                                 reply_markup=ikb_settings(msg, user))


@dp.callback_query_handler(cb_menu.filter(name='settings'))
async def select_settings(_, msg: MyMessage, user: User):
    poster = POSTERS.get('settings')
    if msg.button != 'admin':
        active = users_db.switch_alert(user.id, msg.button)
    else:
        active = users_db.switch_admin(user.id)
    status = "ВКЛЮЧЕНЫ" if active[0] == 1 else "ОТКЛЮЧЕНЫ"
    match msg.button:
        case 'stream':
            caption = f'Оповещения на все стримы {status}'
        case 'courses':
            caption = f'Оповещения о курсах {status}'
        case 'news':
            caption = f'Оповещения о новостях {status}'
        case _:
            caption = f'Права администратора: {status}'

    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id,
                                 message_id=msg.message_id,
                                 reply_markup=ikb_settings(msg, user))


@dp.callback_query_handler(cb_menu.filter(button='links'))
async def links_list(_, msg: MyMessage, user: User):
    poster = POSTERS.get('links')
    caption = 'Полезные ссылки проекта Dirty Python'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id,
                                 message_id=msg.message_id,
                                 reply_markup=ikb_links(user))
