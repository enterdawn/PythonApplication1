import pymysql
import sqlite3
import sys
import hashlib
import pymssql 
import getpass
import string
import hashlib
pymysql.install_as_MySQLdb()
print("请选择数据库类型（1.mysql 2. MS sql server 3.sqlite）")
sqlsecert=int(input())
while 1:
    if sqlsecert==1:
        try:
            conn = pymysql.connect(host='106.14.147.48', user='homework', passwd="1234567890", db='homework')
        except:
            print("无法连接到数据库,请重新选择")
            continue
        else:break
    elif sqlsecert==2: 
        try:conn = pymssql.connect(host='127.0.0.1',user='sa',password='hello',database='NPKW',charset="utf8")
        except:
            print("无法连接到数据库,请重新选择")
            continue
        else:break
    elif sqlsecert==3:
        con = sqlite3.connect('ticket.db')
    else:
        print("输入错误，请重新输入（1.mysql 2. MS sql server 3.sqlite）")
cur = conn.cursor()




#admin
#功能：
#1.封禁、解封账号
#2.授予管理账户权限
#3.验证票务信息
#4.删除票务信息
#5.修改票务信息
#6.修改用户信息
#7.查看用户信息

#管理员菜单
def admin_menu(username):
    print("管理员你好,%s",username)
    print("1.封禁、解封账号")
    print("2.管理账户权限")
    print("3.验证票务信息")
    print("4.删除票务信息")
    print("5.修改票务信息")
    print("6.修改用户信息")
    print("7.查看用户信息")

def ban_unseal(flag,username):
    if flag==true: 
        cur.execute("update user set statuss = false where username = %s",username)
    else:
        cur.execute("update user set statuss = true where username = %s",username)

#1.封禁、解封账号
def admin_ban_unseal():
    name = ""
    print("请输入要操作的用户名")
    name = input()
    cur.execute("SELECT statuss FROM user where username=%s",name)
    if cur == NULL:
        print("用户不存在")
    elif cur == true:
        select = ""
        print("用户已被封禁，是否解封（是Y/否N）")
        if select == "Y":
            ban_unseal(true,name)
    elif cur == false:
        select = ""
        print("是否封禁该用户（是Y/否N）")
        if select == "Y":
            ban_uneal(false,name)


#2.管理账户权限
def admin_authority():
    name = ""
    print("请输入要给予权限的账户名")
    name = input()
    cur.execute("SELECT admin FROM user where username=%s",name)
    if cur == NULL:
        print("用户不存在")
    elif cur == true:
        print("该用户已经具备管理员权限")
    else:
        cur.execute("update user set admin = true where username = %s",name)
        print("权限授予成功")

#3.验证票务信息
def admin_verify_ticket():
    cur.execute("select * from ticket where verify = 0")
    ind = 1
    flag = [0]
    for val in cur:
        print(ind,end = "")
        print(val)
        flag.append(0)
        ind = ind + 1
    print("请选择已验证的票务信息序号，以#号结束")
    IN = 0
    while str.isdigit(str(IN)) == 1:
        flag[int(IN)] = 1
        IN = input()
    ind = 1
    temp = cur
    for val in cur:
        print("update ticket set verify = 1 where ticketid = %s",val.ticketid)
        if flag[ind] == 1:
            cur.execute("update ticket set verify = 1 where ticketid = %s",val.ticketid)
            print("update ticket set verify = 1 where ticketid = %s",val.ticketid)
        ind = ind + 1


        
    


#用户操作
def admin_operation():
    select = -1
    admin_menu()
    while true:
        select = input()
        if isdigit(select) == false or select < 0 or select > 7:
            print("输入有误，请重新输入")
        else:
            break
    if select == 1:
        admin_ban_unseal()
    elif select == 2:
        admin_authority()
    elif select == 3:
        admin_verify_ticket()
    elif select == 4:
        admin_select_ticket()
    elif select == 5:
        admin_modify_ticket()
    elif select == 6:
        admin_modify_user()
    elif select == 7:
        admin_view_user()



#user
#login

def resigner():
    print("请输入用户名")
    cur.execute("SELECT userpassword FROM user where username=%s",username)
    if cur!=NULL :print("用户已存在")

admin_verify_ticket()
while 1:
    print("请输入用户名（输入resigner注册）:")
    username=input()
    if username==resigner: resigner()
    password=getpass.getpass("请输入密码:")
    md5pass = hashlib.md5(password.encode("utf-8"))
    md5password = md5pass.hexdigest()
    cur.execute("SELECT userpassword FROM user where username=%s",username)
    if cur is None :print("用户不存在")
    for i in cur:
        print(i)
        print(md5password)
        if i[0]!=md5password:print("密码错误")



for r in cur:
  print(r)
cur.close()
conn.close()