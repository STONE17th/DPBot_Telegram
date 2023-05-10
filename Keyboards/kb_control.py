from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def kb_control(options: str = '') -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)

    btn_next = KeyboardButton(text='Дальше')
    btn_lect = KeyboardButton(text='Лекция')
    btn_semi = KeyboardButton(text='Семинар')
    btn_cancel = KeyboardButton(text='Отмена')
    if options == 'only_cancel':
        keyboard.add(btn_cancel)
    elif options == 'lect_semi':
        keyboard.row(btn_lect, btn_semi)
        keyboard.add(btn_next, btn_cancel)
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
