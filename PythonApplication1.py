import pymysql
import sqlite3
import pymssql 
pymysql.install_as_MySQLdb()
print("请选择数据库类型（1.mysql 2. MS sql server 3.sqlite）")
sqlsecert=int(input())
while 1:
    if sqlsecert==1:
        try:conn = pymysql.connect(host='106.14.147.48', user='homework', passwd="1234567890", db='homework')
        except:print("无法连接到数据库,请重新选择")
        else:break
    elif sqlsecert==2: 
        try:conn = pymssql.connect(host='127.0.0.1',user='sa',password='hello',database='NPKW',charset="utf8")
        except:print("无法连接到数据库,请重新选择")
        else:break
    elif sqlsecert==3:
        con = sqlite3.connect('ticket.db')
    else:
        print("输入错误，请重新输入（1.mysql 2. MS sql server 3.sqlite）")
cur = conn.cursor()
#select
#admin
#user
#login
cur.execute("SELECT userid FROM user")
for r in cur:
  print(r)
cur.close()
conn.close()