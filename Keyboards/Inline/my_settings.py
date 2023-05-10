from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

from Classes import MyMessage, User
from Keyboards.Callback import cb_menu
from loader import users_db, settings_db


def ikb_settings(msg: MyMessage, user: User) -> InlineKeyboardMarkup:
    on, off = '\u2705', '\u274C'

    def crt_cb(button: str) -> str:
        return cb_menu.new(name='settings', button=button)

    def btn_switch_admin() -> InKB:
        _, _, active, *_ = users_db.get(user.id)
        text = (on if active == 1 else off) + ': Admin'
        return InKB(text=text, callback_data=crt_cb('admin'))

    keyboard = InlineKeyboardMarkup(row_width=2)
    *_, stream, courses, news, _, _ = users_db.get(user.id)
    btn_alert_list = [(':Стримы', on if stream == 1 else off, 'stream'),
                      (':Мои курсы', on if courses == 1 else off, 'courses'),
                      (':Новости', on if news == 1 else off, 'news')]
    btn_pict = InKB(text='Постеры', callback_data=cb_menu.new(name='main', button='pict'))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='main', button='back'))

    keyboard.row(*[InKB(text=f'{switch}{text}', callback_data=crt_cb(button))
                   for text, switch, button in btn_alert_list])

    if user.is_admin:
        keyboard.add(btn_switch_admin(), btn_pict, btn_back)
    else:
        keyboard.add(btn_back)
    return keyboard


def ikb_links(user: User) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    link_list = {link[4]: link[3] for link in settings_db.load('link')}
    for text, link in link_list.items():
        keyboard.insert(InKB(url=link, text=text))
    btn_add = InKB(text='Обновить', callback_data=cb_menu.new(name='', button='setup_links'))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='back'))
    if user.is_active_admin:
        keyboard.add(btn_add, btn_back)
        return keyboard
    keyboard.add(btn_back)
    return keyboard
