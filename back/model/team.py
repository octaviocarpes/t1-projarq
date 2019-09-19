

class Team:
    def __init__(self, team_name, admin_name):
        self.team_name = team_name
        self.admin_name = admin_name
        self.members = []

    def add_member(self, member_name):
        self.members.append(member_name)

    def add_members(self, members):
        self.members.extend(members)

    def remove_member(self, member_name):
        try:
            self.members.remove(member_name)
        except ValueError:
            pass

    def remove_members(self, members):
        for member in members:
            self.remove_member(member)

