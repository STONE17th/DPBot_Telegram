from loader import courses_db
from .lecture import Lecture


class Course:
    def __init__(self, data: tuple, full: bool = False):
        self.table_name = data[1]
        self.name = data[2]
        self.description = data[3]
        self.poster = data[4]
        self.tg_id = data[5]
        self.tg_url = data[6]
        self.lectures_seminars = data[7]
        self.start_date = data[8]
        self.price = data[9]
        self.finished = data[10]
        self.lecture = [Lecture(lecture, self.table_name)
                        for lecture in courses_db.lecture(self.table_name, full)]

    @property
    def quantity(self) -> int:
        return sum(map(int, self.lectures_seminars.split(':')))

    @property
    def progress(self) -> str:
        all_lectures = courses_db.lecture(self.table_name, True)
        total = len(all_lectures)
        done = len([1 for lecture in all_lectures if lecture[-1]])
        return f'Завершен: {round(done / total * 100, 1)}% ({done}/{total})'

    @property
    def is_done(self):
        all_lectures = courses_db.lecture(self.table_name, True)
        return all([(lambda x: x[-1] == 1)(item) for item in all_lectures])

    @property
    def button(self):
        return self.name + (' (Лекции)' if self.finished else ' (Онлайн)')

    def info(self, full: bool = False):
        return f'{self.name}\n\n{self.description}\n\nДата начала курса: {self.start_date}' \
               f'\n\nЦена курса: {self.price} руб'
