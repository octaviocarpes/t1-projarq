import sqlite3
from model.team import Team


class TeamsDB:

    def add_team(self, team_name, admin_name):
        query = f'INSERT INTO TEAM VALUES ("{team_name}", "{admin_name}");'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query).fetchall()
                return True

            except sqlite3.IntegrityError:
                return False
            except sqlite3.OperationalError:
                return False

    def get_team(self, team_name):
        query = f'SELECT * FROM TEAM WHERE team_name = "{team_name}";'

        with sqlite3.connect('database/local.db') as conn:
            return self.create_team(conn.cursor().execute(query).fetchall())

    def add_members(self, team_name, members):
        query = f'INSERT INTO STUDENT_TEAM VALUES ("{team_name}", '

        with sqlite3.connect('database/local.db') as conn:
            try:
                for member in members:
                    conn.cursor().execute(query + f'"{member}");')

                return True
            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    def remove_member(self, team_name, member):
        query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND username = "{member}"'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True

            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    def remove_members(self, team_name, members):
        query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND username = '

        with sqlite3.connect('database/local.db') as conn:
            try:
                for member in members:
                    conn.cursor().execute(query + f'"{member}";')

                return True

            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    def remove_team(self, team_name):
        first_query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}";'
        second_query = f'DELETE FROM TEAM WHERE team_name = "{team_name}";'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(first_query)
                conn.cursor().execute(second_query)
                return True

            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    @staticmethod
    def create_team(query_response):
        if not query_response:
            return None

        return Team(query_response[0], query_response[1])
