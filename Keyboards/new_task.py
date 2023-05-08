from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from loader import tasks_db


def kb_new_task(level: bool = False) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if level:
        type_list = [task_type[0] for task_type in tasks_db.collect('task_type')]
        btn_list = [KeyboardButton(text=task_type) for task_type in set(type_list)]
    else:
        btn_list = [KeyboardButton(text=level) for level in ['easy', 'normal', 'hard']]
    btn_cancel = KeyboardButton(text='Отмена')
    keyboard.add(*btn_list)
    keyboard.add(btn_cancel)
    return keyboard
