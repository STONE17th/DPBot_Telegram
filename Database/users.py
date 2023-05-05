from .database import DataBase


class Users(DataBase):

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users 
        (user_id INT AUTO_INCREMENT,
        tg_id INT,
        admin INT,
        alert_stream INT,
        alert_course INT,
        alert_news INT,
        courses VARCHAR(100),
        lectures VARCHAR(100),
        PRIMARY KEY (user_id),
        UNIQUE KEY telegram_id (tg_id))'''
        self.execute(sql, commit=True)

    def check(self, user_id: int):
        sql = f'''SELECT * FROM users WHERE tg_id={user_id}'''
        if not self.execute(sql, fetchone=True):
            new_user = (user_id, 0, 1, 1, 1, None, None)
            sql = f'''INSERT INTO users 
            (tg_id, admin, alert_stream, alert_course, alert_news, courses, lectures) 
            VALUES (?, ?, ?, ?, ?, ?, ?)'''
            self.execute(sql, new_user, commit=True)

    def get(self, tg_id: int) -> tuple:
        sql = '''SELECT * FROM users WHERE tg_id=?'''
        return self.execute(sql, (tg_id,), fetchone=True)
