from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

from Keyboards.Callback import cb_menu


def ikb_purchase_done(url: str = '') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    btn_courses_my = InKB(text='Мои курсы', callback_data=cb_menu.new(name='', button='courses_my'))
    if url:
        btn_url = InKB(text='Группа в TG', url=url) if url else None
        keyboard.row(btn_main, btn_url, btn_courses_my)
    else:
        keyboard.row(btn_main, btn_courses_my)
    return keyboard
