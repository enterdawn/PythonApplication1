import pymysql
import sqlite3
import sys
import hashlib
import pymssql 
import getpass
import string
import hashlib
import time
import re
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
        try:conn = pymssql.connect(host='175.24.8.61',user='sa',password='homework123.',database='homework',charset="utf8")
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
    print("管理员",username,"你好")
    print("1.封禁、解封账号")
    print("2.管理账户权限")
    print("3.验证票务信息")
    print("4.删除票务信息")
    print("5.修改票务信息")
    print("6.修改用户信息")
    print("7.查看用户信息")
    print("8.退出系统")


#1.封禁、解封账号
def admin_ban_unseal():
    name = ""
    print("请输入要操作的用户名")
    name = input()
    cur.execute("SELECT statuss FROM users where username=%s",name)
    ok = 0
    status = ""
    for val in cur:
        ok = 1
        status = val
    if ok == 0:
        print("用户不存在")
    else:
        if status[0] == 1:
            select = ""
            print("用户已被封禁，是否解封（是y/否n）")
            select = input()
            if select == "y":
                cur.execute("update users set statuss = 0 where username = %s",name)
                conn.commit()
                print("操作成功")
        else:
            select = ""
            print("是否封禁该用户（是y/否n）")
            select = input()
            if select == "y":
                cur.execute("update users set statuss = 1 where username = %s",name)
                conn.commit()
                print("操作成功")


#2.管理账户权限
def admin_authority():
    name = ""
    print("请输入要给予权限的账户名")
    name = input()
    cur.execute("SELECT admin FROM users where username=%s",name)
    ok = 0
    admin = 0
    for val in cur:
        ok = 1
        admin = val
    if ok == 0:
        print("用户不存在")
    else:
        if admin[0] == 1:
            print("该用户已经具备管理员权限")
        else:
            cur.execute("update users set admin = true where username = %s",name)
            conn.commit()
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

#4.删除票务信息
def admin_delete_ticket():
    ticketid = -1
    print("请输入要删除的票务编号")
    while 1:
        ticketid = input()
        if ticketid == "#":
            return 
        cur.execute("select * from ticket where ticketid = %s",ticketid)
        info = cur.fetchall()
        if len(info) == 0:
            print("该票务未查到,请重新输入(输入#返回上级菜单)")
        else:
            break
    print("您确定要删除此项记录？(是y/否n)")
    ok = input()
    if ok == "y":
        cur.execute("delete from ticket where ticketid = %s",ticketid)
        conn.commit()
        print("删除成功")


#5.修改班次信息
def admin_modify_order():
    orderid = -1
    print("请输入要修改的班次编号")
    while 1:
        orderid = input()
        if orderid == "#":
            return 
        cur.execute("select * from classticket where orderid = %s",orderid)
        info = cur.fetchall()
        if len(info) == 0:
            print("该班次未找到，请重新输入班次编号(输入#返回上级菜单)")
        else:
            break;
    print("可修改项如下")
    while 1:
        print("类型、上传者编号、余量、公司、出发地、目的地、开始时间、历时、当前价格、状态")
        print("请输入要修改的数据项(以“++”结束输入)")
        select = input()
        if(select == "++"):
            break
        val = input()
        info = [val,orderid]
        if select == "类型":
            cur.execute("update classticket set typee = %s where orderid = %s",info)
        if select == "上传者编号":
            cur.execute("update classticket set uploaderid = %s where orderid = %s",info)
        if select == "余量":
            cur.execute("update classticket set rest = %s where orderid = %s",info)
        if select == "公司":
            cur.execute("update classticket set company = %s where orderid = %s",info)
        if select == "出发点":
            cur.execute("update classticket set fromm = %s where orderid = %s",info)
        if select == "目的地":
            cur.execute("update classticket set too = %s where orderid = %s",info)
        if select == "开始时间":
            cur.execute("update classticket set begintime = %s where orderid = %s",info)
        if select == "历时":
            cur.execute("update classticket set timee = %s where orderid = %s",info)
        if select == "当前价格":
            cur.execute("update classticket set money = %s where orderid = %s",info)
        if select == "状态":
            cur.execute("update classticket set statuss = %s where orderid = %s",info)
        conn.commit()
        print("数据更新成功")



#6.修改用户信息
def admin_modify_user():
    username = -1
    print("请输入要修改的用户名")
    while 1:
        username = input()
        if username == "#":
            return 
        cur.execute("select * from users where username = %s",username)
        info = cur.fetchall()
        if len(info) == 0:
            print("该用户未找到，请重新输入用户名(输入#返回上级菜单)")
        else:
            break;
    print("可修改项如下")
    while 1:
        select,val = "",""
        print("密码、姓名、性别、手机号、电子邮箱、活跃度、身份证号、账户状态、管理权限")
        print("请输入要修改的数据项(以“++”结束输入)")
        select = input()
        if select == "++" :
            break
        if select == "密码":
           fpw = getpass.getpass("请输入新密码")
           spw = getpass.getpass("请确认密码")
           while fpw != spw:
               fpw = getpass.getpass("请输入新密码")
               spw = getpass.getpass("请确认密码")
           md5pass = hashlib.md5(fpw.encode("utf-8"))
           md5password = md5pass.hexdigest()
           val = md5password
        if select == "性别":
            val == input()
            while val != "男" and val != "女":
                print("输入有误，请重新输入")
                val = input()
        if select == "手机号":
            val = input()
            phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
            pg = true
            while re.search(phone_pat,val) == 0:
                print("输入有误，请重新输入")
                val = input()

        if select == "电子邮箱":
            val = input()
            email_pat = re.compile('^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
            while re.search(email_pat,val) == 0:
                print("输入有误，请重新输入")
                val = input()
        if select == "管理权限":
            cur.execute("select admin from users where username = %s",username)
            info = cur.fetchall()
            print("enter",info[0][0])
            if info[0] == 0:
                val = 1
            else:
                val = 0
        if select == "账户状态":
            cur.execute("select statuss from users where username = %s",username)
            info = cur.fetchall()
            if info == 0:
                val = 1
            else:
                val =0
        if select != "账户状态" and select != "管理权限" and select != "电子邮箱" and select != "手机号" and select != "性别" and select != "密码":
            val = input()
        info = [val,username]
        if select == "密码":
            cur.execute("update users set userpassword = %s where username = %s",info)
        if select == "姓名":
            cur.execute("update users set namee = %s where username = %s",info)
        if select == "性别":
            cur.execute("update users set sex = %s where username = %s",info)
        if select == "手机号":
            cur.execute("update users set phonenumber = %s where username = %s",info)
        if select == "电子邮箱":
            cur.execute("update users set email = %s where username = %s",info)
        if select == "活跃度":
            cur.execute("update users set active = %s where username = %s",info)
        if select == "身份证号":
            cur.execute("update users set idcard = %s where username = %s",info)
        if select == "账户状态":
            cur.execute("update users set statuss = %s where username = %s",info)
        if select == "管理权限":
            cur.execute("update users set admin = %s where username = %s",info)
        conn.commit()
        print("数据更新成功")
    print("\n最新数据如下")
    admin_view_user(username)

#7.查看用户信息
def admin_view_user(username):
    cur.execute("select * from users where username = %s",username)
    info = cur.fetchall()
    ind = 1
    for val in info[0]:
        if ind == 1:
            print("用户编号: ",end="")
        if ind == 2:
            print("用户名: ",end="")
        if ind == 3:
            ind = ind + 1
            continue
        if ind == 4:
            print("用户姓名: ",end="")
        if ind == 5:
            print("性别: ",end="")
        if ind == 6:
            print("手机号: ",end="")
        if ind == 7:
            print("电子邮箱: ",end="")
        if ind == 8:
            print("活跃度: ",end="")
        if ind == 9:
            print("身份证号: ",end="")
        if ind == 10:
            print("账户状态: ",end="")
        if ind == 11:
            print("管理权限: ",end="")
        if ind == 12:
            print("注册时间: ",end="")
        print(val)
        ind = ind + 1





#管理员用户操作

def admin_operation(username):
    while 1:
        select = ""
        admin_menu(username)
        while 1:
            select = input()
            if select.isdigit() == 0 or select < str(0) or select > str(8):
                print("输入有误，请重新输入")
            else:
                break
        if select == "1":
            admin_ban_unseal()
        elif select == "2":
            admin_authority()
        elif select == "3":
            admin_verify_ticket()
        elif select == "4":
            admin_delete_ticket()
        elif select == "5":
            admin_modify_order()
        elif select == "6":
            admin_modify_user()
        elif select == "7":
            print("请输入要查询用户名")
            username = input()
            admin_view_user()
        else:
            break;



#user
#def user_operation(username):

#login
#注册

def register():
    print("请输入用户名")
    flag = 0
    while 1:
        enter = 0
        registername=input()
        cur.execute("SELECT username FROM users where username=%s",registername)
        for i in cur:
            enter = 1
            if i or registername == "register" :
                print("用户已存在,请重新输入用户名")
            else:
               flag=1
        if flag == 1 or enter == 0:
            break
    now = int(round(time.time()*1000))
    registertime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now/1000))
    cur.execute("SELECT MAX(userid) from users")
    for i in cur:
         userid=int(i[0])+1
    while 1:
        password=getpass.getpass("请输入密码:")
        if len(password)<6 :print("密码太短,请重新输入")
        elif len(password)>20:print("密码太长，请重新输入")
        else:break
    md5pass = hashlib.md5(password.encode("utf-8"))
    md5password = md5pass.hexdigest()
    print("请输入您的姓名")
    name=input()
    print(username,",",name,",","确定注册(y,n)？")
    y=input()
    if y=="y":
        info = [userid,registername,md5password,name]
        cur.execute("INSERT INTO users(userid, username,userpassword,namee) VALUES (%s,%s,%s,%s);",info)
        conn.commit()
        print("注册成功")


#1.发布信息
#2.修改自己信息
#3.查询票务信息
#4.删除发布的票务信息
#5.退出系统
#普通用户

def user_publish():
    print("empty")

def user_modify():
    print("empty")

def user_search():
    print("empty")

def user_delete():
    print("empty")


def user_opmenu():
    print("1.发布票务信息\n2.修改个人信息\n3.查询票务信息\n4.删除发布的票务信息")

def user_operation(username):
    print("用户",username,"你好")
    while 1:
        user_opmenu()
        select = input()
        if select == 1:
            user_publish()
        if select == 2:
            user_modify()
        if select == 3:
            user_search()
        if select == 4:
            user_delete()
        if select == 5:
            break

#admin_verify_ticket()
while 1:
    print("请输入用户名（输入register注册）:")
    username=input()
    if username=="register":
        register()
        continue
    password=getpass.getpass("请输入密码:")
    md5pass = hashlib.md5(password.encode("utf-8"))
    md5password = md5pass.hexdigest()
    cur.execute("SELECT userpassword FROM users where username=%s",username)
    for i in cur:
        if i[0]!=md5password:
            print("密码错误")
            continue
        else:
            cur.execute("SELECT admin FROM users where username=%s",username)
            for i in cur:
                if i[0]==1: 
                    admin_operation(username)
                else:
                    user_operation(username)


for r in cur:
  print(r)
cur.close()
conn.close()


