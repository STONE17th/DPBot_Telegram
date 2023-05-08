from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

from Classes import User, MyMessage
from Keyboards.Callback import navigation, cb_menu


def crt_cb(menu: str, task_type: str, task_level: str = '', current_id: int = 0) -> str:
    return navigation.new(menu=menu, type=task_type, level=task_level, id=current_id)


def cid(size: int, current_id: int, direction: int) -> int:
    prev_id = (current_id - 1) if current_id != 0 else (size - 1)
    next_id = (current_id + 1) if current_id != (size - 1) else 0
    if direction:
        return next_id
    return prev_id


def ikb_select_type(btn_list: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_list = [InKB(text=btn, callback_data=crt_cb('level', btn)) for btn in btn_list]
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='back'))
    keyboard.row(*btn_list)
    keyboard.row(btn_back)
    return keyboard


def ikb_select_level(btn_list: list[str], task_type: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_list = [InKB(text=btn, callback_data=crt_cb('task', task_type, btn)) for btn in btn_list]
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    btn_back = InKB(text='Назад', callback_data=navigation.new(menu='types', type='', level='', id=0))
    keyboard.row(*btn_list)
    keyboard.row(btn_main, btn_back)
    return keyboard


def ikb_select_task(size: int, user: User, msg: MyMessage) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_prev = InKB(text='<<<', callback_data=crt_cb('task', msg.type, msg.level, cid(size, msg.id, 0)))
    btn_next = InKB(text='>>>', callback_data=crt_cb('task', msg.type, msg.level, cid(size, msg.id, 1)))
    btn_task_delete = InKB(text='Удалить задачу', callback_data=crt_cb('task_delete', msg.type, msg.level, msg.id))
    btn_main = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    btn_back = InKB(text='Назад', callback_data=crt_cb('level', msg.type, msg.level))
    if size > 1:
        keyboard.add(btn_prev, btn_next)
    if user.is_active_admin:
        keyboard.add(btn_task_delete, btn_main, btn_back)
    else:
        keyboard.add(btn_main, btn_back)
    return keyboard
