import sqlite3
from model.team import Team


class TeamsDB:

    def add_team(self, team_name, admin_name):
        first_query = f'INSERT INTO TEAM VALUES ("{team_name}", "{admin_name}", 0.0);'
        second_query = f'INSERT INTO STUDENT_TEAM VALUES ("{team_name}", "{admin_name}");'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(first_query)
                conn.cursor().execute(second_query)
                return True

            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    def add_member(self, team_name, username):
        query = f'INSERT INTO STUDENT_TEAM VALUES ("{team_name}", "{username}");'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True

            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    def add_members(self, team_name, members):
        query = f'INSERT INTO STUDENT_TEAM VALUES ("{team_name}", '

        with sqlite3.connect('database/local.db') as conn:
            error_index = 0
            try:
                for member in members:
                    conn.cursor().execute(query + f'"{member}");')
                    error_index += 1

                return True

            except sqlite3.IntegrityError:
                query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND username = '

                for member in members[:error_index]:
                    try:
                        conn.cursor().execute(query + f'"{member}";')

                    except Exception:
                        pass

                return False

            except sqlite3.OperationalError:
                query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND username = '

                for member in members[:error_index]:
                    try:
                        conn.cursor().execute(query + f'"{member}";')

                    except Exception:
                        pass

                return False

    def get_user_team(self, username):
        query = f'SELECT * FROM STUDENT_TEAM WHERE username = "{username}";'

        with sqlite3.connect('database/local.db') as conn:
            return self.create_team(conn.cursor().execute(query).fetchall()[0], [])

    def get_team(self, team_name):
        first_query = f'SELECT * FROM TEAM WHERE team_name = "{team_name}";'
        second_query = f'SELECT * FROM STUDENT_TEAM WHERE team_name = "{team_name}";'

        with sqlite3.connect('database/local.db') as conn:
            team = conn.cursor().execute(first_query).fetchall()[0]
            members = conn.cursor().execute(second_query).fetchall()
            return self.create_team(team, members)

    def get_teams(self):
        query = f'SELECT * FROM TEAM;'

        with sqlite3.connect('database/local.db') as conn:
            teams = conn.cursor().execute(query).fetchall()
            teams_objects = []
            for team_name, admin_name, rank in teams:
                members = conn.cursor().execute(f'SELECT * FROM STUDENT_TEAM WHERE team_name = "{team_name}";').fetchall()
                teams_objects.append(self.create_team((team_name, admin_name, rank), members))

            return teams_objects

    def get_rank(self):
        query = f'SELECT * FROM TEAM ORDER BY rank DESC;'

        with sqlite3.connect('database/local.db') as conn:
            teams = conn.cursor().execute(query).fetchall()
            teams_objects = []
            for team in teams:
                teams_objects.append(self.create_team(team, []))

            return teams_objects

    def update_rank(self, team_name, rank):
        query = f'UPDATE TEAM SET rank = "{rank}" WHERE team_name = "{team_name}";'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
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

    def remove_member(self, team_name, member):
        query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND username = "{member}";'

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
            error_index = 0
            try:
                for member in members:
                    conn.cursor().execute(query + f'"{member}";')
                    error_index += 1

                return True

            except sqlite3.IntegrityError:
                query = f'INSERT INTO STUDENT_TEAM VALUES("{team_name}", '

                for member in members[:error_index]:
                    conn.cursor().execute(query + f'"{member}");')

                return False

            except sqlite3.OperationalError:
                query = f'INSERT INTO STUDENT_TEAM VALUES("{team_name}", '

                for member in members[:error_index]:
                    conn.cursor().execute(query + f'"{member}");')

                return False

    def create_team(self, team, members):
        if not team:
            return None

        t = Team(*team[:2])
        t.add_members([member for _, member in members])

        return t
