
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

            sql = "select IFNULL(TICKER,0),IFNULL(PRC, 0),IFNULL(prediction, 0),IFNULL(date, 0) from stockprice where date between DATE_SUB('{}', INTERVAL 8 DAY)  and  '{}' and TICKER = '{}' ;".format(time,time,stock)
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
            connection.close()
    if result == None:
        print(None)
    else:
        #print(result)
        price = []
        prediction = []
        date = []
        for one in result:

            price.append(one[1])
            #mod_date = time.strptime(one[2], "%Y-%m-%d")
            prediction.append(one[2])
            mod_day = one[3].split( )[0]
            date.append(mod_day)

        #print(price)
        #print(date)
        dic = {
        "price": price,
        "prediction": prediction,
        "date": date
    }
    
    return dic


def get_stock_lounge_month(stock,time):

    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select IFNULL(TICKER,0),IFNULL(PRC, 0),IFNULL(prediction, 0), IFNULL(date, 0) from stockprice where date between DATE_SUB('{}', INTERVAL 31 DAY)  and  '{}' and TICKER = '{}' ;".format(time,time,stock)
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
        prediction = []
        for one in result:

            price.append(one[1])
            #mod_date = time.strptime(one[2], "%Y-%m-%d")
            prediction.append(one[2])
            mod_day = one[3].split( )[0]
            date.append(mod_day)

        #print(price)
        #print(date)
        dic = {
        "price": price,
        "prediction": prediction,
        "date": date
    }
    
    return dic

def get_stock_lounge_year(stock,time):

    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select IFNULL(TICKER,0),IFNULL(PRC, 0),IFNULL(prediction, 0), IFNULL(date, 0) from stockprice where date between DATE_SUB('{}', INTERVAL 365 DAY)  and  '{}' and TICKER = '{}' ;".format(time,time,stock)
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
        prediction = []
        for one in result:

            price.append(one[1])
            #mod_date = time.strptime(one[2], "%Y-%m-%d")
            prediction.append(one[2])
            mod_day = one[3].split( )[0]
            date.append(mod_day)

        #print(price)
        #print(date)
        dic = {
        "price": price,
        "prediction": prediction,
        "date": date
    }
    
    return dic


def get_All_Stock():

    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select TICKER, COMNAM, PERMNO, words from company_stock natural join CPSP_ticker natural join feature;"
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
            mylist[count]=[row[0],row[1],row[2],row[3]]
            count+=1
    return mylist

def get_Recomd(time):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

    try:
        with connection.cursor() as cursor:

            sql = "select A.TICKER, PERMNO, concat(round(10*(A.PRC-B.PRC)/B.PRC,4),'%'), A.PRC from stockprice as A, stockprice as B natural join CPSP_ticker where A.date='{}' and B.date=if(A.date like '2000-01%', '2000-01-03', DATE_SUB(A.date, INTERVAL 30 DAY)) and A.TICKER=B.TICKER order by (A.PRC-B.PRC)/A.PRC desc limit 10;".format(time)
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

print(get_Recomd('2011-02-03'))

def money_enough(stock,quantity,email,time):
    
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    try:
        with connection.cursor() as cursor:
            sql="select user_id,balance,PRC from users,stockprice where email='{}' and date='{}' and TICKER='{}' and balance > PRC*{};".format(email,time,stock,quantity)
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
            connection.close()

    if bool(result)== False:
        return False
    else:
        return True

def quantity_enough(stock,quantity,email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    try:
        with connection.cursor() as cursor:
            sql="SELECT user_id,email,TICKER,sum(volume) FROM users natural join store group by user_id,TICKER having  email='{}' and TICKER='{}' and sum(volume) >={};".format(email,stock,quantity)
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
            connection.close()
    if bool(result)==False:
        return False
    else:
        return True



def get_buy(time,stock,quantity,email):
    
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    sql = 'INSERT INTO transaction_records(user_id,time,TICKER,price,volume) select user_id ,date, TICKER, PRC,{} FROM users, stockprice where email="{}" and  date="{}" and TICKER="{}";'.format(quantity,email,time,stock)
    sql0= "update users natural join transaction_records set users.balance= users.balance-transaction_records.price*transaction_records.volume  where users.email='{}' and transaction_records.time='{}' and transaction_records.TICKER='{}';".format(email,time,stock)
    sql1='insert into store(user_id,TICKER,volume) select user_id,TICKER, {} FROM users, stockprice where email="{}" and  date="{}" and TICKER="{}";'.format(quantity,email,time,stock)
    
    try:
        with connection.cursor() as cursor:

            cursor.execute(sql)
            cursor.execute(sql0)
            cursor.execute(sql1)
            connection.commit()
    finally:
        connection.close()

def get_sell(time,stock,quantity,email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    sql = 'INSERT INTO transaction_records(user_id,time,TICKER,price,volume) select user_id,date, TICKER, PRC,-{} FROM users, stockprice where email="{}" and  date="{}" and TICKER="{}";'.format(quantity,email,time,stock)
    sql0= "update users natural join transaction_records set users.balance= users.balance-transaction_records.price*transaction_records.volume  where users.email='{}' and transaction_records.time='{}' and transaction_records.TICKER='{}';".format(email,time,stock)
    sql1='insert into store(user_id,TICKER,volume) select user_id,TICKER, -{} FROM users, stockprice where email="{}" and  date="{}" and TICKER="{}";'.format(quantity,email,time,stock)
    try:
        with connection.cursor() as cursor:

            cursor.execute(sql)
            cursor.execute(sql0)            
            cursor.execute(sql1)

            connection.commit()
    finally:
        connection.close()

def transac_records(email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    try:
        with connection.cursor() as cursor:

            sql = "SELECT time,TICKER,price,volume FROM transaction_records natural join users where email='{}';".format(email)
            
            cursor.execute(sql)
            
            result = cursor.fetchall()
    finally:
            connection.close()
    
    if bool(result) ==False:
        return None
    else:
        my_record=""
        for i in range(len(result)):
            my_record+='<tr> <td>'+str(i+1)+"</td><td>"+str(result[i][0])+"</td><td>"+str(result[i][1])+"</td><td>"+str(result[i][2])+"</td><td>"+str(result[i][3])+"</td></tr>"
    return my_record

def get_balance(email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    try:
        with connection.cursor() as cursor:

            sql = "SELECT balance FROM users where email='{}';".format(email)
            
            cursor.execute(sql)
            
            result = cursor.fetchall()
    finally:
            connection.close()
    
    if result ==False:
        return None
    else:
        return str(result[0][0])

def get_rank(email):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    try:
        with connection.cursor() as cursor:

            sql = "select t.rank from (SELECT email,balance, CASE WHEN @prevRank = balance THEN @curRank WHEN @prevRank := balance THEN @curRank := @curRank + 1 END AS rank FROM users, (SELECT @curRank :=0, @prevRank := NULL) r ORDER BY balance desc) as t where email='{}';".format(email)
            
            cursor.execute(sql)
            
            result = cursor.fetchall()
    finally:
            connection.close()
    
    if result ==False:
        return None
    else:
        return str(result[0][0])

def get_portfolio_list(email,time):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    try:
        with connection.cursor() as cursor:

            sql = "select ticker, sum(volume), PRC, round(sum(volume)*PRC,4) from transaction_records natural join users natural join stockprice where email='{}' and date=if('{}'>'2018-12-31','2018-12-31','{}') group by ticker;".format(email,time,time)
            
            cursor.execute(sql)
            
            result = cursor.fetchall()
    finally:
            connection.close()
    
    if len(result)==0:
        return None
    else:
        myhtml=''
        count=1
        for i in range(len(result)):
            if result[i][1]==0:
                continue
            else:
                myhtml+='<tr><td>'+str(count)+'</td><td>'+result[i][0]+'</td><td>'+str(result[i][1])+'</td><td>'+str(result[i][2])+'</td><td>'+str(result[i][3])+'</td></tr>'
                count+=1
        return myhtml

def get_yield(email,time):
    connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
    try:
        with connection.cursor() as cursor:

            sql = "select sum(volume)*PRC from transaction_records natural join users natural join stockprice where email='{}' and date=if('{}'>'2018-12-31','2018-12-31','{}') group by ticker;".format(email,time,time)
            cursor.execute(sql)
            result1 = cursor.fetchall()
            sql = "select balance from users where email='{}';".format(email)
            cursor.execute(sql)
            result2 = cursor.fetchall()
            
    finally:
            connection.close()
    
    if len(result1)==0:
        return None
    else:
        rate=0
        balance=float(result2[0][0])
        for i in range(len(result1)):
            rate+=float(result1[i][0])
        rate=100*(rate+balance-1000000)/1000000
        rate=round(rate,4)
        return str(rate)+'%'

