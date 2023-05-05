from .database import DataBase


class Courses(DataBase):

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS courses 
        (course_id INT AUTO_INCREMENT,
        table_name VARCHAR(20),
        name VARCHAR(50),
        description VARCHAR(500),
        poster VARCHAR(150),
        tg_url VARCHAR(50),
        disc_url VARCHAR(50),
        quantity INT,
        start_date VARCHAR(10),
        price INT,
        finished INT,
        PRIMARY KEY (course_id))'''
        self.execute(sql, commit=True)

    def create_course_table(self, table: str):
        sql = f'''CREATE TABLE IF NOT EXISTS course_{table}
        (lecture_id INT AUTO_INCREMENT,
        name VARCHAR(50),
        description VARCHAR(500),
        poster VARCHAR(150),
        lect_url VARCHAR(50),
        semi_url VARCHAR(50),
        comp_url VARCHAR(50),
        date VARCHAR(10),
        price INT,
        finished INT,
        PRIMARY KEY (lecture_id))'''
        self.execute(sql, commit=True)

    @property
    def is_finished(self):
        if self.is_finished == 1:
            return True
        elif self.is_finished == 0:
            return False
        else:
            return 'Архив'

    def add(self, data: dict[str, str | int]):
        new_course = (data.get('table_name'), data.get('name'), data.get('description'),
                      data.get('poster'), data.get('tg_url'), data.get('disc_url'),
                      data.get('quantity'), data.get('start_date'), data.get('price'), 0)
        sql = f'''INSERT INTO courses (table_name, name, description, poster, tg_url, disc_url, 
        quantity, start_date, price, finished) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, new_course, commit=True)
        self.create_course_table(data.get('table_name'))
        new_lecture = (None, None, data.get('poster'), None, None, None, None, None, 0)
        sql = f'''INSERT INTO course_{data.get('table_name')} (name, description, poster, lect_url, 
        semi_url, comp_url, date, price, finished) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        for _ in range(int(data.get('quantity'))):
            self.execute(sql, new_lecture, commit=True)

    def load(self, table_name: str = '') -> tuple | list[tuple]:
        if table_name:
            sql = '''SELECT * FROM courses WHERE table_name=?'''
            return self.execute(sql, (table_name,), fetchone=True)
        sql = '''SELECT * FROM courses'''
        return self.execute(sql, fetchall=True)

    def lecture(self, table_name: str, index: int = 0) -> tuple | list[tuple]:
        if index:
            sql = f'''SELECT * FROM course_{table_name} WHERE lecture_id={index+1}'''
            return self.execute(sql, fetchone=True)
        sql = f'''SELECT * FROM course_{table_name}'''
        return self.execute(sql, fetchall=True)

