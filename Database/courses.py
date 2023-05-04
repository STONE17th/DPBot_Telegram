from .database import DataBase


class Courses(DataBase):

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS courses 
        (course_id INT AUTO_INCREMENT PRIMARY KEY,
        table_name VARCHAR(20),
        name VARCHAR(50),
        description VARCHAR(50),
        poster VARCHAR(50),
        tg_address VARCHAR(50),
        disk_address VARCHAR (50),
        quantity INT,
        start VARCHAR(10),
        price INT,
        finished INT)'''
        print(sql.__repr__())
        self.execute(sql, commit=True)
