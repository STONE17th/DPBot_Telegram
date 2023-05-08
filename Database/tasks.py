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

    def collect(self, task_type: str = None, task_level: str = None) -> tuple:
        sql = 'SELECT task_type FROM tasks'
        params = ()
        if task_type:
            sql = f'SELECT task_level FROM tasks WHERE task_type=?'
            params = (task_type,)
        if task_level:
            sql = f'SELECT * FROM tasks WHERE task_type=? AND task_level=?'
            params = (task_type, task_level)
        return self.execute(sql, params, fetchall=True)
