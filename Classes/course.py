from loader import courses_db
from .lecture import Lecture


class Course:
    def __init__(self, data: tuple, full: bool = False):
        self.table_name = data[1]
        self.name = data[2]
        self.description = data[3]
        self.poster = data[4]
        self.tg_url = data[5]
        self.disc_url = data[6]
        self.quantity = data[7]
        self.start_date = data[8]
        self.price = data[9]
        self.finished = data[10]
        lectures = courses_db.lecture(self.table_name, full)
        self.lecture = [Lecture(lecture, self.table_name) for lecture in lectures]

    @property
    def progress(self) -> str:
        all_lectures = courses_db.lecture(self.table_name, True)
        total = len(all_lectures)
        done = len([1 for lecture in all_lectures if lecture[-1]])
        return f'Завершен: {round(done / total * 100, 1)}% ({done}/{total})'

    @property
    def is_done(self):
        all_lectures = courses_db.lecture(self.table_name)
        return all([(lambda x: x[-1] == 1)(item) for item in all_lectures])


    @property
    def button(self):
        return self.name + (' (Лекции)' if self.finished else ' (Онлайн)')

    def info(self, full: bool = False):
        if full:
            return f'{self.name}\n\n{self.description}\n\nРабочая группа: {self.tg_url}\nОблако Яндекс: ' \
                   f'{self.disc_url}\n\nДата начала курса: {self.start_date}\n\nЦена курса: {self.price} руб'
        return f'{self.name}\n\n{self.description}\n\nДата начала курса: {self.start_date}' \
               f'\n\nЦена курса: {self.price} руб'
