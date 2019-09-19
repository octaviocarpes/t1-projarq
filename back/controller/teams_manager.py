from model.team import Team
from model.teams_database import TeamsDB


class TeamsManager:
    def __init__(self):
        self.teams = {}
        self.teams_db = TeamsDB()

    def create_team(self, team_name, admin_name):
        if team_name not in self.teams.keys():
            if self.teams_db.add_team(team_name, admin_name):
                self.teams[team_name] = Team(team_name, admin_name)
                return True

        return False

    def add_members(self, team_name, admin_name, members):
        if team_name in self.teams.keys():
            if admin_name == self.teams[team_name].admin_name:
                if self.teams_db.add_members(team_name, members):
                    self.teams[team_name].add_members(members)
                    return True
            else:
                return False

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_name == admin_name:
                self.teams[team_name] = team
                if self.teams_db.add_members(team_name, members):
                    self.teams[team_name].add_members(members)
                    return True
                else:
                    return False
            else:
                return False

    def delete_member(self, team_name, admin_name, member):
        if team_name in self.teams.keys():
            if self.teams[team_name].admin_name == admin_name:
                self.teams[team_name].remove_member(member)
                return self.teams_db.remove_member(team_name, member)

            return False

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_name == admin_name:
                return self.teams_db.remove_member(team_name, member)

            return False

    def delete_members(self, team_name, admin_name, members):
        if team_name in self.teams.keys():
            if self.teams[team_name].admin_name == admin_name:
                self.teams[team_name].remove_members(members)
                return self.teams_db.remove_members(team_name, members)

            return False

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_name == admin_name:
                return self.teams_db.remove_members(team_name, members)

            return False

    def delete_team(self, team_name, admin_name):
        if team_name in self.teams.keys():
            if self.teams[team_name].admin_name == admin_name:
                del self.teams[team_name]
                return self.teams_db.remove_team(team_name)

            else:
                return False

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_name == admin_name:
                return self.teams_db.remove_team(team_name)

            else:
                return False
