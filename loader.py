from os import getenv
from aiogram import Bot, Dispatcher

from Database import Courses, Users


bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)
courses_db = Courses()
users_db = Users()

