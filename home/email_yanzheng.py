#!/usr/bin/env python
#coding:utf-8
from random import Random # 用于生成随机码 
from django.core.mail import send_mail # 发送邮件模块
from home.models import EmailVerify,Emailsports # 邮箱验证model
from sportcases.settings import EMAIL_FROM  # setting.py添加的的配置信息
import datetime

# 生成6位随机字符串
def random_str(randomlength=6):
    print(random_str)
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    #print(str)
    return str

#发送活动内容
def send_sportcontent_email(email,sporttitle,sportcontent,sportlink):
    print("send_sportcontent_email")
    email_sports= Emailsports()
    #将给用户发的信息保存在数据库中  
    email_sports.email = email
    email_sports.emailsporttitle = sporttitle
    email_sports.emailsportcontent = sportcontent
    email_sports.emailsportlink = sportlink 
    email_sports.create_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    email_sports.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    email_title = "活动： "+str(sporttitle)
    email_body = "通知： 活动" +str(sporttitle)+" 已经发布,请大家踊跃报名.活动链接为: "+str(sportlink)+" " + str(sportcontent) 

    # 发送邮件
    print(email_body)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass
    return 1

#发送修改密码验证码
def send_uppassword_email(email, send_type="uppassword"):
    print(send_uppassword_email)
    email_record = EmailVerify()
    #将给用户发的信息保存在数据库中
    code = random_str(6)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.create_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    if send_type == "uppassword":
        email_title = "修改密码通知"
        email_body = "温馨提醒：您正在修改密码，请在验证码输入框中输入："+code+" ，以完成操作。"
        # 发送邮件
        print(email_body)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "checkEmail":
        email_title = "验证邮箱通知"
        email_body = "温馨提醒：您正在验证邮箱，请在验证码输入框中输入："+code+" ，以完成操作。"
        # 发送邮件
        print(email_body)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

def send_succ_email(email, send_type="uppasswordsucc"):
    email_title = "修改密码通知"
    email_body = "鹧鸪网提醒：您密码修改成功，请妥善保管！祝您愉快！"
    # 发送邮件
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass