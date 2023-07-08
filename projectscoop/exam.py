# import MySql.connector
# from MySql.connector import Error

# def connect():
#     conn=MySql.connector.connect(host='localhost',database='exam',user='root',password='')
#     cur=conn.cursor()
# def insert():
#     cur.execute("insert into  values('eno','name',sal)")
#     conn.commit()
#     print("recorrd")
# insert()
import random
print(random.randrange(0,20))