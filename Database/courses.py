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
        tg_id INT,
        tg_url VARCHAR(50),
        lect_semi VARCHAR(5),
        start_date VARCHAR(10),
        price INT,
        finished INT,
        PRIMARY KEY (course_id))'''
        self.execute(sql, commit=True)

    def create_course_table(self, table: str):
        sql = f'''CREATE TABLE IF NOT EXISTS course_{table}
        (lecture_id INT AUTO_INCREMENT,
        lect_semi INT,
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

    def name(self, table_name: str) -> tuple[str]:
        sql = 'SELECT name FROM courses WHERE table_name=?'
        return self.execute(sql, (table_name,), fetchone=True)[0]

    def add(self, data: dict[str, str | int]):
        new_course = (data.get('table_name'), data.get('name'), data.get('description'),
                      data.get('poster'), data.get('lect_semi'), data.get('start_date'), data.get('price'), 2)
        sql = f'''INSERT INTO courses (table_name, name, description, poster, lect_semi, start_date, price, finished) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute(sql, new_course, commit=True)
        self.create_course_table(data.get('table_name'))
        new_lecture = (0, None, None, data.get('poster'), None, None, None, None, 0, 0)
        sql = f'''INSERT INTO course_{data.get('table_name')} (lect_semi, name, description, poster, lect_url, 
        semi_url, comp_url, date, price, finished) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        for _ in range(sum(map(int, data.get('lect_semi').split(':')))):
            self.execute(sql, new_lecture, commit=True)

    def load(self, table_name: str = '') -> tuple | list[tuple]:
        if table_name:
            sql = '''SELECT * FROM courses WHERE table_name=?'''
            return self.execute(sql, (table_name,), fetchone=True)
        sql = '''SELECT * FROM courses'''
        return self.execute(sql, fetchall=True)

    def activate_tg(self, table_name: str, chat_id: int, invite_link: str):
        sql = 'UPDATE courses SET tg_url=?, tg_id=?, finished=? WHERE table_name=?'
        self.execute(sql, (invite_link, chat_id, 0, table_name), commit=True)

    def update(self, data: tuple, table_name: str, index: int):
        sql = f'''UPDATE course_{table_name} SET lect_semi=?, name=?, description=?, poster=?, lect_url=?, semi_url=?, 
        comp_url=?, date=?, price=?, finished=? WHERE lecture_id=?'''
        params = data + (1, index + 1)
        self.execute(sql, params, commit=True)

    def finalize(self, table_name: str):
        sql = '''UPDATE courses SET finished = finished + 1 WHERE table_name=?'''
        self.execute(sql, (table_name,), commit=True)

    def select(self, table_name: str) -> tuple:
        sql = '''SELECT * FROM courses WHERE table_name=?'''
        return self.execute(sql, (table_name,), fetchone=True)

    def lecture(self, table_name: str, admin: bool = False, index: int = -1) -> tuple | list[tuple]:
        if index >= 0:
            sql = f'''SELECT * FROM course_{table_name} WHERE lecture_id={index}'''
            return self.execute(sql, fetchone=True)
        sql = f'''SELECT * FROM course_{table_name}''' + ('' if admin else ' WHERE finished = 1')
        return self.execute(sql, fetchall=True)

    def my_purchase(self, table_name: str, index: int = -1) -> tuple:
        if index >= 0:
            sql = f'''SELECT * FROM course_{table_name} WHERE lecture_id=?'''
            return self.execute(sql, (index,), fetchone=True)
        sql = 'SELECT * FROM courses WHERE table_name=?'
        return self.execute(sql, (table_name,), fetchone=True)
