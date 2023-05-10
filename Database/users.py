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
        alert_courses INT,
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
            (tg_id, admin, alert_stream, alert_courses, alert_news, courses, lectures) 
            VALUES (?, ?, ?, ?, ?, ?, ?)'''
            self.execute(sql, new_user, commit=True)

    def get(self, tg_id: int) -> tuple:
        sql = '''SELECT * FROM users WHERE tg_id=?'''
        return self.execute(sql, (tg_id,), fetchone=True)



    def courses_and_lectures(self, tg_id: int) -> tuple[str]:
        sql = 'SELECT courses, lectures FROM users WHERE tg_id=?'
        return self.execute(sql, (tg_id,), fetchone=True)

    def purchase(self, tg_id: int, target: str):
        targ = 'lectures' if ':' in target else 'courses'
        sql = f'SELECT {targ} FROM users WHERE tg_id=?'
        cur = self.execute(sql, (tg_id,), fetchone=True)[0]
        cur = cur if cur else ''
        sql = f'''UPDATE users SET {targ} = ? WHERE tg_id=?'''
        self.execute(sql, (target + ' ' + cur, tg_id), commit=True)

    def add_course(self, user_id: int, chat_id: int):
        sql = 'SELECT name, poster, table_name FROM courses WHERE tg_id=?'
        name, poster, table_name = self.execute(sql, (chat_id,), fetchone=True)
        sql = 'SELECT courses FROM users WHERE tg_id=?'
        user_courses = self.execute(sql, (user_id,), fetchone=True)[0]
        if user_courses:
            if table_name not in user_courses:
                user_courses = ' '.join([table_name.strip(), user_courses.strip()])
            else:
                return False, poster, 'Этот курс тебе уже добавлен'
        else:
            user_courses = table_name
        sql = 'UPDATE users SET courses=? WHERE tg_id=?'
        self.execute(sql, (user_courses, user_id), commit=True)
        return True, poster, f'Тебе добавлен курс {name}'


    def switch_alert(self, tg_id: int, option: str) -> tuple:
        sql = f'''UPDATE users SET alert_{option} = CASE WHEN alert_{option} = 1 
        THEN 0 ELSE 1 END WHERE tg_id=?'''
        self.execute(sql, (tg_id,), commit=True)
        sql = f'''SELECT alert_{option} FROM users WHERE tg_id=?'''
        return self.execute(sql, (tg_id,), fetchone=True)

    def switch_admin(self, tg_id: int):
        sql = f'''UPDATE users SET admin = CASE WHEN admin = 1
        THEN -1 ELSE 1 END WHERE tg_id=?'''
        self.execute(sql, (tg_id,), commit=True)
        sql = f'''SELECT admin FROM users WHERE tg_id=?'''
        return self.execute(sql, (tg_id,), fetchone=True)

    def alerts(self, **kwargs):
        alert = kwargs.get('alert')
        table = kwargs.get('table')
        if not table:
            sql = f'''SELECT tg_id FROM users WHERE {alert}=1'''
            return self.execute(sql, fetchall=True)
        sql = f'''SELECT tg_id FROM users  WHERE {alert}=1 AND courses LIKE "%{table}%"'''
        return self.execute(sql, fetchall=True)

    def set_admin(self, tg_id: int):
        sql = 'UPDATE users SET admin = 1 WHERE tg_id=?'
        self.execute(sql, (tg_id,), commit=True)
