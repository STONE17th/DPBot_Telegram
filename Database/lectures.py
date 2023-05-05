from .database import DataBase


class Lectures(DataBase):

    def __init__(self):
        super().__init__()

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
