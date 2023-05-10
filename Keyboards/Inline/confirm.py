from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

from Keyboards.Callback.callback import confirm, cb_menu, navigation


def ikb_confirm(target: str, args: str = '') -> InlineKeyboardMarkup:
    def crt_cb(targ: str, args: str, button: str) -> str:
        return confirm.new(menu=targ, args=args, button=button)

    keyboard = InlineKeyboardMarkup(row_width=2)

    btn_yes = InKB(text='Да', callback_data=crt_cb(target, args, 'yes'))
    btn_no = InKB(text='Нет', callback_data=crt_cb(target, args, 'no'))
    if target == 'task':
        btn_yes = InKB(text='Да', callback_data=cb_menu.new(name='', button='add_task'))
        btn_no = InKB(text='В меню', callback_data=cb_menu.new(name='', button='back'))
    keyboard.add(btn_yes, btn_no)

    return keyboard
