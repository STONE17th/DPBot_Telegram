class Lecture:
    def __init__(self, data: tuple, table_name: str):
        self.table_name = table_name
        self.name = data[1]
        self.description = data[2]
        self.poster = data[3]
        self.lect_url = data[4]
        self.semi_url = data[5]
        self.comp_url = data[6]
        self.date = data[7]
        self.price = data[8]
        self._finished = data[9]

    @property
    def is_finished(self):
        return True if self._finished else False

    def info(self, full: bool = False):
        if full:
            return f'{self.name}\n\n{self.description}\n\nЛекция: {self.lect_url}\nСеминар: {self.semi_url}\n' \
                   f'Конспект: {self.comp_url}\n\nЦена лекции: {self.price} руб'
        return f'{self.name}\n\n{self.description}\n\nЦена лекции: {self.price} руб'
