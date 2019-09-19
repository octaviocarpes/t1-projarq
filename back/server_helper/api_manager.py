import sqlite3
from controller.users_manager import UsersManager
from controller.teams_manager import TeamsManager
from controller.certificates_manager import CertificatesManager
from server_helper.json_encoder import Encoder


class Manager:
    def __init__(self):
        self.users_manager = UsersManager()
        self.teams_manager = TeamsManager()
        self.certificates_manager = CertificatesManager()
        self.json_encoder = Encoder()
        try:
            sqlite3.connect('database/local.db').execute(open('database/script.sql', 'r').read())
        except sqlite3.OperationalError:
            pass

    def check_user(self, username, password, is_student):
        return self.users_manager.check_user(username, password, is_student)

    def add_student(self, username, password, course):
        return self.users_manager.add_user(username, password, True, course)

    def add_valuer(self, username, password):
        return self.users_manager.add_user(username, password, False, '')

    def rate_team(self, valuer_name, team_name, software, pitch, innovation, team):
        return self.teams_manager.rate_team(valuer_name, team_name, software, pitch, innovation, team)

    def get_teams(self):
        return self.teams_manager.get_teams()

    def get_team(self, team_name):
        return self.teams_manager.get_team(team_name)

    def create_team(self, team_name, admin_name):
        return self.teams_manager.create_team(team_name, admin_name)

    def add_members(self, team_name, admin_name, members):
        software_engineer_counter = 0
        for member in members:
            student = self.users_manager.get_user(member, True)
            if student is None:
                return False

            if student.course == 'ES':
                software_engineer_counter += 1

            if software_engineer_counter == 5:
                return False

        return self.teams_manager.add_members(team_name, admin_name, members)

    def delete_team(self, team_name, admin_name):
        return self.teams_manager.delete_team(team_name, admin_name)

    def get_teams_rank(self):
        return self.teams_manager.get_rank()

    def generate_certificate(self, student_name):
        return self.certificates_manager.generate_certificate(student_name)
