
##@login_manager.user_loader
##def load_user(user_id):
##    return User.query.get(int(user_id))



def User(username, email, password):
    return "INSERT INTO users(username,email,user_password)VALUES('{}','{}','{}');".format(username,email,password)

def Get_password(email):
    return "SELECT user_password FROM users WHERE email='{}';".format(email)