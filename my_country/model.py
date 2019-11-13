
##@login_manager.user_loader
##def load_user(user_id):
##    return User.query.get(int(user_id))

import pymysql.cursors

def User(username, email, password):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    sql = "INSERT INTO users(username,email,user_password)VALUES('{}','{}','{}');".format(username,email,password)
    try:
        with connection.cursor() as cursor:

            cursor.execute(sql)
        
            connection.commit()
    finally:
            connection.close()



def Get_password(email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "SELECT user_password FROM users WHERE email='{}';".format(email)
            cursor.execute(sql)
            result = cursor.fetchone()
    finally:
            connection.close()
    return result[0]


def already_exist(username, email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    sql = "select * from users where username='{}' or email ='{}';".format(username,email)
    try:
        with connection.cursor() as cursor:

            cursor.execute(sql)
            result = cursor.fetchone()
    finally:
        connection.close()

    if result == None:
        return False

    return True