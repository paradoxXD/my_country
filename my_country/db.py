import pymysql.cursors

connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")

try:

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM tasks"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()