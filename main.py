from aiogram.utils import executor

import Middleware
from Handlers import dp
from loader import courses_db, settings_db, streams_db, tasks_db, users_db
from temp import load_temp


async def on_start(_):
    print('Dirty Bot started!')
    try:
        courses_db.create_table()
        settings_db.create_table()
        streams_db.create_table()
        tasks_db.create_table()
        users_db.create_table()
        print('Database... OK!!!')
        # load_temp()
    except:
        print('Database... FAILURE')
    load_temp()

if __name__ == '__main__':
    Middleware.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)

