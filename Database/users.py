from .database import DataBase


class Users(DataBase):

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users 
        (user_id INT AUTO_INCREMENT PRIMARY KEY, tg_id INT, admin INT,
        alert_stream INT, alert_course INT, alert_news INT,
        courses VARCHAR(100), lectures VARCHAR(100))'''
        self.execute(sql, commit=True)
