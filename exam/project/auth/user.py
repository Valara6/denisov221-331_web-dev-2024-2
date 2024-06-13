from flask_login import UserMixin


rights = ["view", "create", "edit", "delete"]


admin = [rights[0], rights[1], rights[2], rights[3]]
moderator = [rights[0], rights[2]]
user = [rights[0]]


rightsArr = [admin, moderator, user]








class User(UserMixin):
    def __init__(self, userid, login, firstname, lastname, second_name, role_id):
        self.id = userid
        self.login = login
        self.first_name = firstname
        self.last_name = lastname
        self.second_name = second_name
        self.role_id = role_id

    def UserRights(self, action):
        return action in rightsArr[self.role_id - 1]




