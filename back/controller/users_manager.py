from model.valuer import Valuer
from model.student import Student
from model.users_database import UsersDB


class UsersManager:
    def __init__(self):
        self.students = {}
        self.valuers = {}
        self.users_database = UsersDB()

    def add_user(self, username, password, is_student, course):
        if is_student:
            if username not in self.students.keys():
                if self.users_database.add_student(username, password, course):
                    self.students[username] = Student(username, password, course)
                    return True

            return False

        else:
            if username not in self.valuers.keys():
                if self.users_database.add_valuer(username, password):
                    self.valuers[username] = Valuer(username, password)
                    return True

            return False

    def check_user(self, username, password, is_student):
        if is_student:
            if username not in self.students.keys():
                student = self.users_database.get_student(username)
                if student is not None:
                    self.students[username] = student
                    return student.password == password

                return False

            return self.students[username].password == password

        else:
            if username not in self.valuers.keys():
                valuer = self.users_database.get_valuer(username)
                if valuer is not None:
                    self.valuers[username] = valuer
                    return valuer.password == password

                return False

            return self.valuers[username].password == password

    def get_user(self, username, is_student):
        if is_student:
            if username not in self.students.keys():
                return self.users_database.get_student(username)

            return self.students[username]

        else:
            if username not in self.valuers.keys():
                return self.users_database.get_valuer(username)

            return self.valuers[username]