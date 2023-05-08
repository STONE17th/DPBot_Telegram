from os import getenv

from mysql.connector import connect


class DataBase:

    def __init__(self, user: str = getenv('USER'), password: str = getenv('PASSWORD')):
        self.user = user
        self.password = password

    @property
    def connection(self):
        return connect(host="bot_network:3306",
                       user=self.user,
                       password=self.password,
                       database='stone_db')

    def execute(self, sql: str, parameters: tuple = tuple(),
                fetchone=False, fetchall=False, commit=False):
        connection = self.connection
        cursor = connection.cursor(prepared=True)
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        # cursor.close()
        connection.close()
        return data

    @staticmethod
    def extract_kwargs(sql: str, parameters: dict) -> tuple:
        sql += ' AND '.join([f'{key} = ?' for key in parameters])
        return sql, tuple(parameters.values())

    def disconnect(self):
        self.connection.close()
