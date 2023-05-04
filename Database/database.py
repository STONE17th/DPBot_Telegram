from os import getenv
from mysql.connector import connect, Error


class DataBase:

    def __init__(self, user: str = getenv('USER'), password: str = getenv('PASSWORD')):
        self.user = user
        self.password = password

    @property
    def connection(self):
        return connect(host="localhost", user=self.user, password=self.password, database='dp_db')

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            self.connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def extract_kwargs(sql: str, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())

    def disconnect(self):
        self.connection.close()
