from aiogram.types import Message, CallbackQuery, ChatInviteLink

from Classes import MyMessage, User
from Keyboards import kb_control, ikb_confirm, ikb_user_notification
from Keyboards.Callback import cb_menu
from loader import dp, bot, courses_db, users_db
from Misc import user_notify


@dp.message_handler(commands=['activate'])
async def activate_chat(message: Message):
    table_name = message.text.split()[1]
    chat_id = message.chat.id
    invite: ChatInviteLink = await bot.create_chat_invite_link(chat_id)
    # try:
    courses_db.activate_tg(table_name, chat_id, invite.invite_link)
        # await message.answer('Группа TG успешно активирована')
    # except:
    #     await message.answer('Ошибка при активации группы')


@dp.message_handler(commands=['add_me'])
async def activate_chat(message: Message):
    chat_id = message.chat.id
    ans = users_db.add_course(message.from_user.id, chat_id)
    await bot.send_photo(chat_id=message.from_user.id, photo=ans[1], caption=ans[2],
                         reply_markup=ikb_user_notification('courses', '') if ans[0] else None)


