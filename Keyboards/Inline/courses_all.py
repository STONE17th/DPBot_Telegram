from aiogram.types import InlineKeyboardButton as InKB, InlineKeyboardMarkup

from Classes import User
from Keyboards.Callback import cb_menu, course_navigation
from temp import load_courses


def crt_cb(target: str = '', table: str = '', current_id: int = 0):
    return course_navigation.new(menu=target, table=table, current_id=current_id)


def cid(size: int, current_id: int, direction: int) -> int:
    prev_id = (current_id - 1) if current_id != 0 else (size - 1)
    next_id = (current_id + 1) if current_id != (size - 1) else 0
    if direction:
        return next_id
    return prev_id


def ikb_all_courses(admin: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_online = []
    btn_offline = []
    all_courses = load_courses()
    if all_courses:
        for course in all_courses.values():
            if course.finished < 2:
                if admin or course.finished == 1:
                    btn = InKB(text=course.button,
                               callback_data=crt_cb('offline', course.table_name))
                    btn_offline.append(btn)
                else:
                    btn = InKB(text=course.button,
                               callback_data=crt_cb('online', course.table_name))
                    btn_online.append(btn)
    btn_create_new_course = InKB(text='Создать', callback_data=cb_menu.new(name='', button='new_course'))
    btn_individual = InKB(text='Индивидуальные занятия', callback_data=cb_menu.new(name='', button='individual'))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='back'))
    keyboard.add(*btn_online)
    keyboard.add(*btn_offline)
    if admin:
        keyboard.row(btn_create_new_course, btn_back)
    else:
        keyboard.row(btn_individual, btn_back)
    return keyboard


def ikb_off_course(user: User, menu: str, table: str, current_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    all_courses = load_courses()
    course = all_courses.get(table)
    # lecture = course.lecture[current_id]
    size = course.quantity

    btn_prev = InKB(text='<<<', callback_data=crt_cb(menu, table, cid(size, current_id, 0)))
    btn_next = InKB(text='>>>', callback_data=crt_cb(menu, table, cid(size, current_id, 1)))
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='courses_all'))

    btn_edit = InKB(text='Изменить', callback_data=crt_cb('edit_lecture', table, current_id))
    btn_finalize = InKB(text='Завершить', callback_data=crt_cb('finalize_course', table, current_id))
    btn_archive = InKB(text='Архивировать', callback_data=crt_cb('finalize_course', table, -1))
    btn_purchase = InKB(text='Купить', callback_data=crt_cb('purchase', table, current_id))

    if size > 1:
        keyboard.row(btn_prev, btn_next)
    if user.is_admin:
        if course.is_done:
            if course.finished == 1:
                keyboard.row(btn_archive)
            elif course.finished == 0:
                keyboard.row(btn_finalize)
        keyboard.add(btn_edit, btn_main, btn_back)
    else:
        if (user.courses and table in user.courses) or \
                (user.lectures and f'{table}:{current_id + 1}' in user.lectures):
            keyboard.row(btn_main, btn_back)
        else:
            keyboard.row(btn_purchase, btn_main, btn_back)
    return keyboard


def ikb_on_course(user: User, table: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn_purchase = InKB(text='Купить', callback_data=crt_cb('purchase', table, -1))
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='courses_all'))
    if user.courses and table in user.courses:
        keyboard.row(btn_main, btn_back)
    else:
        keyboard.row(btn_purchase)
        keyboard.row(btn_main, btn_back)
    return keyboard


def ikb_individual() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_want = InKB(text='Оставить заявку', callback_data=crt_cb('want'))
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    keyboard.add(btn_want, btn_main)
    return keyboard
