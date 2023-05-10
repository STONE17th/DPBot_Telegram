from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

from Keyboards.Callback import cb_menu, navigation


def crt_cb(button: str):
    return cb_menu.new(name='main', button=button)


def ikb_start(admin: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)

    btn_tasks = InKB(text='Задачи', callback_data=navigation.new(menu='types', type='', level='', id=0))
    btn_all_courses = InKB(text='Курсы DP', callback_data=crt_cb('courses_all'))
    btn_my_courses = InKB(text='Мои курсы', callback_data=crt_cb('courses_my'))
    btn_my_settings = InKB(text='Настройки', callback_data=crt_cb('my_settings'))
    btn_notification = InKB(text='Создать...', callback_data=crt_cb('notification'))
    btn_links = InKB(text='Ссылки', callback_data=crt_cb('links'))

    keyboard.add(btn_tasks, btn_all_courses, btn_notification if admin else btn_my_courses)
    keyboard.add(btn_my_settings, btn_links)

    return keyboard


def ikb_main():
    keyboard = InlineKeyboardMarkup(row_width=1)
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    keyboard.add(btn_main)
    return keyboard
