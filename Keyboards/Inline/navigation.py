from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

from Keyboards.Callback import navigation


def crt_cb(menu: str, task_type: str, task_level: str = '', current_id: int = 0) -> str:
    return navigation.new(top=menu, mid=task_type, low=task_level, id=current_id)


def cid(size: int, current_id: int, direction: int) -> int:
    prev_id = (current_id - 1) if current_id != 0 else (size - 1)
    next_id = (current_id + 1) if current_id != (size - 1) else 0
    if direction:
        return next_id
    return prev_id


def ikb_select_task(menu: str, list_item: list, cur_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    size = len(list_item)

    btn_prev = InKB(text='<<<', callback_data=crt_cb(menu, task_type, task_level, cid(size, cur_id, 0)))
    btn_next = InKB(text='>>>', callback_data=crt_cb(menu, task_type, task_level, cid(size, cur_id, 1)))
    btn_back = InKB(text='Назад', callback_data=crt_cb('type', task_type))
    btn_task_delete = InKB(text='Удалить задачу',
                           callback_data=crt_cb('task_delete', task_type, task_level, curr_id))
    if size > 1:
        keyboard.add(btn_prev, btn_next)
    if admin:
        keyboard.add(btn_task_delete, btn_back)
    else:
        keyboard.add(btn_back)
    return keyboard
