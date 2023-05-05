from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import Database

fsm_memory = MemoryStorage()

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot, storage=fsm_memory)
courses_db = Database.Courses()
lectures_db = Database.Lectures()
settings_db = Database.Settings()
streams_db = Database.Streams()
tasks_db = Database.Tasks()
users_db = Database.Users()

