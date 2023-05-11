from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton as InKB

class Lecture:
    def __init__(self, data: tuple, table_name: str):
        self.table_name = table_name
        self.lect_semi = data[1]
        self.name = data[2]
        self.description = data[3]
        self.poster = data[4]
        self.lect_url = data[5]
        self.semi_url = data[6]
        self.comp_url = data[7]
        self.date = data[8]
        self.price = data[9]
        self._finished = data[10]

    @property
    def is_finished(self):
        return True if self._finished else False

    def info(self, price: bool = False):
        prefix = 'Лекция: ' if self.lect_semi == 1 else 'Семинар: '
        suffix = f'\n\nЦена лекции: {self.price} руб' if price else ''
        return prefix + f'{self.name}\n{self.description}' + suffix

    @property
    def buttons(self):
        btn_list = ['Лекция', 'Семинар', 'Конспект']
        url_list = [self.lect_url, self.semi_url, self.comp_url]
        btn_list = [InKB(text=btn_list[i], url=url_list[i]) for i in range(3) if url_list[i]]
        return btn_list
