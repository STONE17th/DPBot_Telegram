from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

from Keyboards.Callback import cb_menu


def ikb_notification() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_stream = InKB(text='Стрим', callback_data=cb_menu.new(name='', button='stream'))
    btn_news = InKB(text='Новость', callback_data=cb_menu.new(name='', button='news'))
    btn_back = InKB(text='Назад', callback_data=cb_menu.new(name='', button='back'))
    keyboard.row(btn_stream, btn_news)
    keyboard.add(btn_back)
    return keyboard


def ikb_user_notification(menu: str, url: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    match menu:
        case 'stream':
            btn_main = InKB(text='Go на cтрим!', url=url)
        case 'courses':
            btn_main = InKB(text='Перейти', callback_data=cb_menu.new(name='main', button='courses_my'))
        case 'news':
            text = 'Перейти' if url else 'Закрепить'
            button = 'all_courses' if url else 'pin_news'
            btn_main = InKB(text=text, callback_data=cb_menu.new(name='main', button=button))
    btn_delete = InKB(text='Удалить', callback_data=cb_menu.new(name='', button='message_delete'))
    keyboard.row(btn_main, btn_delete)
    return keyboard
