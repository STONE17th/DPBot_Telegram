from aiogram.types import InlineKeyboardButton as InKB, InlineKeyboardMarkup

from Keyboards.Callback import cb_menu, course_navigation
from loader import courses_db


def crt_cb(target: str = '', table: str = '', current_id: int = 0):
    return course_navigation.new(menu=target, table=table, current_id=current_id)


def cid(size: int, current_id: int, direction: int) -> int:
    prev_id = (current_id - 1) if current_id != 0 else (size - 1)
    next_id = (current_id + 1) if current_id != (size - 1) else 0
    if direction:
        return next_id
    return prev_id


def ikb_courses_my(courses, lectures) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    if courses:
        btn_courses = [InKB(text=courses_db.select(course)[2],
                            callback_data=crt_cb('courses_my', course)) for course in courses]
        [keyboard.add(btn) for btn in btn_courses]
    if lectures:
        btn_courses = InKB(text='Отдельные лекции', callback_data=crt_cb('courses_my', 'custom'))
        keyboard.add(btn_courses)
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='back'))
    keyboard.add(btn_back)
    return keyboard


def ikb_course_my_navigation(menu: str, buttons: tuple[str, str], curr_id: int, list_size: int,
                             table: str = '') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    btn_prev = InKB(text='<<<', callback_data=crt_cb(menu, table, cid(list_size, curr_id, 0)))
    btn_next = InKB(text='>>>', callback_data=crt_cb(menu, table, cid(list_size, curr_id, 1)))
    if buttons != (None, None, None):
        btn_lect = InKB(text='Лекция', url=buttons[0]) if buttons[0] else None
        btn_semi = InKB(text='Семинар', url=buttons[1]) if buttons[1] else None
        btn_comp = InKB(text='Конспект', url=buttons[2]) if buttons[2] else None
        if btn_lect:
            keyboard.add(btn_lect)
        if btn_semi:
            keyboard.insert(btn_semi)
        if btn_comp:
            keyboard.insert(btn_comp)
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='courses_my'))
    if list_size > 1:
        keyboard.add(btn_prev, btn_next)
    keyboard.add(btn_main, btn_back)
    return keyboard
