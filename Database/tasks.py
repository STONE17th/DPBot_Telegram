from .database import DataBase


class Tasks(DataBase):

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS tasks 
        (task_id INT AUTO_INCREMENT,
        task_type VARCHAR(50),
        task_level VARCHAR(50),
        task VARCHAR(500),
        PRIMARY KEY (task_id))'''
        self.execute(sql, commit=True)
