from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_control(finish: bool = False) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)

    btn_next = KeyboardButton(text='Дальше')
    btn_cancel = KeyboardButton(text='Отмена')
    if finish:
        keyboard.add(btn_cancel)
    else:
        keyboard.add(btn_next, btn_cancel)
    return keyboard


def kb_stream() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_list = [KeyboardButton(text=name) for name in ['YouTube', 'ZOOM']]
    btn_cancel = KeyboardButton(text='Отмена')
    keyboard.add(*btn_list)
    keyboard.add(btn_cancel)
    return keyboard
