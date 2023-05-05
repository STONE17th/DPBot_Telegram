from .database import DataBase


class Settings(DataBase):

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS settings
        (set_id INT AUTO_INCREMENT,
        set_type VARCHAR(20),
        name VARCHAR(50),
        value VARCHAR(500),
        option_one VARCHAR(50),
        option_two VARCHAR(50),
        option_three VARCHAR(50),
        PRIMARY KEY (set_id),
        UNIQUE KEY unique_setting (name))'''
        self.execute(sql, commit=True)

    def set(self, values: tuple):
        values = values * 2
        sql = f'''INSERT INTO settings (set_type, name, value, option_one, option_two, option_three) VALUES 
        (?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE set_type=?, name=?, value=?, option_one=?, 
        option_two=?, option_three=?'''
        self.execute(sql, values, commit=True)

    def load(self, set_type) -> tuple:
        sql = '''SELECT * FROM settings WHERE set_type=?'''
        return self.execute(sql, (set_type,), fetchall=True)
