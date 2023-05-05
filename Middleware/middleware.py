from Classes import MyMessage, User
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from loader import users_db


class AdvancedData(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        data['msg'] = MyMessage(message)
        users_db.check(message.from_user.id)
        user = users_db.get(message.from_user.id)
        data['user'] = User(user, message.from_user.first_name)

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        data['msg'] = MyMessage(call)
        user = users_db.get(call.from_user.id)
        data['user'] = User(user, call.from_user.first_name)
