
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


def get_stock_lounge_month(stock,time):

    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select IFNULL(TICKER,0),IFNULL(PRC, 0), IFNULL(date, 0) from stockprice where date between DATE_SUB('{}', INTERVAL 31 DAY)  and  '{}' and TICKER = '{}' ;".format(time,time,stock)
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

def get_stock_lounge_year(stock,time):

    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select IFNULL(TICKER,0),IFNULL(PRC, 0), IFNULL(date, 0) from stockprice where date between DATE_SUB('{}', INTERVAL 365 DAY)  and  '{}' and TICKER = '{}' ;".format(time,time,stock)
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


def get_All_Stock():

    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select TICKER, COMNAM, PERMNO from company_stock natural join CPSP_ticker;"
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
            connection.close()
    if result == None:
        print(None)
    else:
        #mylist=result
        mylist=dict()
        count=1
        for row in result:
            mylist[count]=[row[0],row[1],row[2]]
            count+=1
    return mylist

def get_Recomd(time):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select A.TICKER, PERMNO, concat(round(10*(A.PRC-B.PRC)/A.PRC,4),'%'), A.PRC from stockprice as A, stockprice as B natural join CPSP_ticker where A.date='{}' and B.date=if(A.date like '2000-01%', '2000-01-03', DATE_SUB(A.date, INTERVAL 30 DAY)) and A.TICKER=B.TICKER order by (A.PRC-B.PRC)/A.PRC desc limit 10;".format(time)
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
            connection.close()
    if result == None:
        return None
    else:
        myhtml=''
        for i in range(10):
            myhtml+='<tr><td>'+str(i+1)+'</td><td>'+result[i][0]+'</td><td>'+str(result[i][1])+'</td><td>'+result[i][2]+'</td><td>'+str(result[i][3])+'</td></tr>'

    return myhtml
