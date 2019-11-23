
##@login_manager.user_loader
##def load_user(user_id):
##    return User.query.get(int(user_id))

import pymysql.cursors
import time


def User(username, email, password, datetime):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    sql = "INSERT INTO users(username,email,user_password,start_time)VALUES('{}','{}','{}','{}');".format(username,email,password,datetime)
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
    if result == None:
        return None
    else:
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


def Time(email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "SELECT start_time FROM users WHERE email='{}';".format(email)
            cursor.execute(sql)
            result = cursor.fetchone()
    finally:
            connection.close()
    if result == None:
        return None
    else:
        return result[0]


def get_stock_lounge_week(stock,time):

    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select IFNULL(TICKER,0),IFNULL(PRC, 0), IFNULL(date, 0) from stockprice where date between DATE_SUB('{}', INTERVAL 8 DAY)  and  '{}' and TICKER = '{}' ;".format(time,time,stock)
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
            connection.close()
    if result == None:
        print(None)
    else:
        #print(result)
        price = []
        date = []
        for one in result:

            price.append(one[1])
            #mod_date = time.strptime(one[2], "%Y-%m-%d")
            mod_day = one[2].split( )[0]
            date.append(mod_day)

        #print(price)
        #print(date)
        dic = {
        "price": price,
        "date": date
    }
    
    return dic



# connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

# try:
#     with connection.cursor() as cursor:

#         sql = "select IFNULL(TICKER,0),IFNULL(PRC, 0), IFNULL(date, 0) from stockprice where date between DATE_SUB('{}', INTERVAL 8 DAY)  and  '{}' and TICKER = '{}' ;".format('2010-03-11 00:00:00','2010-03-11 00:00:00','AAPL')
#         cursor.execute(sql)
#         result = cursor.fetchall()
# finally:
#         connection.close()
# if result == None:
#     print(None)
# else:
#     price = []
#     date = []
#     for one in result:

#         price.append(one[1])
#         #mod_date = time.strptime(one[2], "%Y-%m-%d")
#         mod_day = one[2].split( )[0]
#         date.append(mod_day)

#     dic = {
#         "price": str(price),
#         "date": str(date)
#     }

#     print(dic)