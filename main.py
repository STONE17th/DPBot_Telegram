from aiogram.utils import executor

from Handlers import dp
from loader import courses_db, users_db


async def on_start(_):
    print('Dirty Bot started!')
    courses_db.create_table()
    try:

        users_db.create_table()
        print('Database... OK!!!')
    except:
        print('Database... FAILURE')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
