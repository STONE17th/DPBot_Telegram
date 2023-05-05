from loader import courses_db
from .lecture import Lecture


class Course:
    def __init__(self, data: tuple):
        self.table_name = data[1]
        self.name = data[2]
        self.description = data[3]
        self.poster = data[4]
        self.tg_url = data[5]
        self.disc_url = data[6]
        self.quantity = data[7]
        self.start_date = data[8]
        self.price = data[9]
        self._finished = data[10]
        lectures = courses_db.lecture(self.table_name)
        self.lecture = [Lecture(lecture, self.table_name) for lecture in lectures]

    def is_finished(self):
        return True if self._finished else False

    def button(self):
        return self.name + (' (Лекции)' if self._finished else ' (Онлайн)')
