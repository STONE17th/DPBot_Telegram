from aiogram.types import InlineKeyboardButton as InKB, InlineKeyboardMarkup

from Classes import MyMessage, User
from Keyboards.Callback import cb_menu, course_navigation
from temp import COURSES


def crt_callback(target: str = '', table: str = '', current_id: int = 0):
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
    if COURSES:
        for course in COURSES.values():
            if admin or course.is_finished():
                btn = InKB(text=course.button(),
                           callback_data=crt_callback('offline', course.table_name))
                btn_offline.append(btn)
            else:
                btn = InKB(text=course.button(),
                           callback_data=crt_callback('online', course.table_name))
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
    course = COURSES.get(table)
    lecture = course.lecture[current_id]
    size = course.quantity

    btn_prev = InKB(text='<<<', callback_data=crt_callback(menu, table, cid(size, current_id, 0)))
    btn_next = InKB(text='>>>', callback_data=crt_callback(menu, table, cid(size, current_id, 1)))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(menu='', button='courses_all'))

    btn_edit = InKB(text='Изменить', callback_data=crt_callback('edit_lecture', table, current_id))
    btn_finalize = InKB(text='Завершить', callback_data=crt_callback('finalize_course', table, current_id))
    btn_archive = InKB(text='Архивировать', callback_data=crt_callback('finalize_course', table, -1))
    btn_purchase = InKB(text='Купить', callback_data=crt_callback('purchase', table, current_id))

    if size > 1:
        keyboard.row(btn_prev, btn_next)
    if user.is_admin:
        if course.is_finished():
            keyboard.row(btn_archive)
        else:
            keyboard.row(btn_finalize)
        keyboard.add(btn_edit, btn_back)
    else:
        if table in user.courses or f'{table}:{current_id + 1}' in user.lectures:
            keyboard.row(btn_back)
        else:
            keyboard.row(btn_purchase, btn_back)
    return keyboard


def ikb_on_course(user: User, table: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn_purchase = InKB(text='Купить', callback_data=crt_callback('purchase', table, -1))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='courses_all'))
    if user.courses and table in user.courses:
        keyboard.row(btn_back)
    else:
        keyboard.row(btn_purchase, btn_back)
    return keyboard


# def ikb_individual() -> InlineKeyboardMarkup:
#     keyboard_individual = InlineKeyboardMarkup(row_width=2)
#     btn_want = InKB(text='Оставить заявку', callback_data=crt_callback('want'))
#     btn_back = InKB(text='Назад', callback_data=main_menu.new(menu='', button='all_courses'))
#     keyboard_individual.add(btn_want, btn_back)
#     return keyboard_individual
