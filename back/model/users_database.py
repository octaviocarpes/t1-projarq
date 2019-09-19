import sqlite3
from model.student import Student
from model.valuer import Valuer


class UsersDB:

    def add_student(self, username, password, course):
        query = f'INSERT INTO STUDENT VALUES ("{username}", "{password}", {course});'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True
            except sqlite3.IntegrityError:
                return False
            except sqlite3.OperationalError:
                return False

    def add_valuer(self, username, password):
        query = f'INSERT INTO VALUER VALUES ("{username}", "{password}");'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True
            except sqlite3.IntegrityError:
                return False
            except sqlite3.OperationalError:
                return False

    def get_student(self, username):
        query = f'SELECT * FROM STUDENT WHERE username = "{username}";'

        with sqlite3.connect('database/local.db') as conn:
            return self.create_student(conn.cursor().execute(query).fetchall())

    def get_valuer(self, username):
        query = f'SELECT * FROM VALUER WHERE username = "{username}";'

        with sqlite3.connect('database/local.db') as conn:
            return self.create_valuer(conn.cursor().execute(query).fetchall())

    @staticmethod
    def create_student(query_response):
        if not query_response:
            return None
        return Student(query_response[0], query_response[1], query_response[2])

    @staticmethod
    def create_valuer(query_response):
        if not query_response:
            return None
        return Valuer(query_response[0], query_response[1])

