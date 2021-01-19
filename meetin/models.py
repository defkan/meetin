from flask import current_app
from meetin.init import login_manager, sql_connection,cursor
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    cursor.execute('SELECT * FROM user where userId = %s',(user_id,))
    res = cursor.fetchone()
    return User(res)

class User(UserMixin):

    def __init__(self,input_dict):
        self.id = input_dict['userId']
        self.username = input_dict['username']
        self.email = input_dict['email']

    def __repr__(self):
        res = 'User('+self.username + ',' + self.email + ')'
        return res



