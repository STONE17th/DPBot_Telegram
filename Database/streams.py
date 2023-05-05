from .database import DataBase


class Streams(DataBase):

    def __init__(self):
        super().__init__()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS streams 
        (stream_id INT AUTO_INCREMENT,
        name VARCHAR(50),
        description VARCHAR(500),
        poster VARCHAR(50),
        stream_url VARCHAR(50),
        date VARCHAR(50),
        PRIMARY KEY (stream_id))'''
        self.execute(sql, commit=True)
