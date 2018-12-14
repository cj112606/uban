from django.db import models

# Create your models here.
class staff(models.Model):
    staffnumber = models.CharField(max_length=300,null=True,blank=True)
    staffname = models.CharField(max_length=300,null=True,blank=True)
    staffnamepinyin = models.CharField(max_length=300,null=True,blank=True)
    staffnamepinyinab = models.CharField(max_length=300,null=True,blank=True)
    staffdept = models.TextField(null=True,blank=True)
    staffdeptclass = models.TextField(null=True,blank=True)
    staffunit = models.TextField(null=True,blank=True)
    staffsex = models.TextField(null=True,blank=True)
    staffphone = models.CharField(max_length=300,null=True,blank=True)
    staffemail = models.CharField(max_length=300,null=True,blank=True)
    staffoaccount = models.CharField(max_length=300,null=True,blank=True)
    staffidcard = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "staff"

    def __str__(self): # __unicode__ on Python 2
        return self.staffname

class staffinfo(models.Model):
    staffnumber = models.CharField(max_length=300,null=True,blank=True)
    staffname = models.CharField(max_length=300,null=True,blank=True)
    staffnamepinyin = models.CharField(max_length=300,null=True,blank=True)
    staffnamepinyinab = models.CharField(max_length=300,null=True,blank=True)
    staffdept = models.TextField(null=True,blank=True)
    staffdeptclass = models.TextField(null=True,blank=True)
    staffunit = models.TextField(null=True,blank=True)
    staffsex = models.TextField(null=True,blank=True)
    staffphone = models.CharField(max_length=300,null=True,blank=True)
    staffemail = models.CharField(max_length=300,null=True,blank=True)
    staffoaccount = models.CharField(max_length=300,null=True,blank=True)
    staffidcard = models.CharField(max_length=300,null=True,blank=True)
    staffworkplace = models.TextField(null=True,blank=True)
    staffpw = models.CharField(max_length=300,null=True,blank=True)
    staffclass = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    bz = models.TextField(null=True,blank=True)
    bztime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "staffinfo"

    def __str__(self): # __unicode__ on Python 2
        return self.staffname
        
class deptment(models.Model):
    deptmentnumber = models.CharField(max_length=300,null=True,blank=True)
    deptmentname = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "deptment"

    def __str__(self): # __unicode__ on Python 2
        return self.sdeptmentname

class deptment_staff(models.Model):
    deptmentnumber = models.CharField(max_length=300,null=True,blank=True)
    staffnumber = models.CharField(max_length=300,null=True,blank=True)
    staffclass = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "deptment"

    def __str__(self): # __unicode__ on Python 2
        return self.sdeptmentname

class sportlist(models.Model):
    sportnumber = models.CharField(max_length=300,null=True,blank=True)
    sportname = models.TextField(null=True,blank=True)
    sportcontent = models.TextField(null=True,blank=True)
    sportlink = models.TextField(null=True,blank=True)
    sportauthor =models.TextField(null=True,blank=True)
    sportstartdate = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    sportenddate = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    sporttype = models.TextField(null=True,blank=True)
    is_top = models.TextField(null=True,blank=True)
    toptime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    topcycle = models.TextField(null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "sportlist"

    def __str__(self): # __unicode__ on Python 2
        return self.sportname


class sport_request(models.Model):
    sportnumber = models.CharField(max_length=300,null=True,blank=True)
    requestnumber = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Mata:
        db_table = "sport_request"

    def __str__(self): # __unicode__ on Python 2
        return self.sportnumber

class requestlist(models.Model):
    requestnumber = models.CharField(max_length=300,null=True,blank=True)
    requestname = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    is_top = models.TextField(null=True,blank=True)
    toptime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    topcycle = models.TextField(null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "sport_request"

    def __str__(self): # __unicode__ on Python 2
        return self.sportnumber
'''
class sport_staff(models.Model):
    sportnumber = models.CharField(max_length=300,null=True,blank=True)
    staffnumber = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "sport_staff"

    def __str__(self): # __unicode__ on Python 2
        return self.sportnumber
'''
class sport_staff_request(models.Model):
    sportnumber = models.CharField(max_length=300,null=True,blank=True)
    staffnumber = models.CharField(max_length=300,null=True,blank=True)
    requestnumber = models.CharField(max_length=300,null=True,blank=True)
    sport_staff_request_info = models.CharField(max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failreason = models.TextField(null=True,blank=True)
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "sport_staff_request"

    def __str__(self): # __unicode__ on Python 2
        return self.staffnumber
class userVisitInfo(models.Model):
    user_visit_ip = models.CharField(max_length=300,null=True,blank=True)   
    user_visit_cookies = models.TextField(null=True,blank=True)
    user_visit_terminal_type = models.TextField(null=True,blank=True)
    user_visit_form  = models.TextField(null=True,blank=True)
    user_visit_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "userVisitInfo"

    def __str__(self): # __unicode__ on Python 2
        return self.user_visit_ip
        
class EmailVerify(models.Model):
    email = models.CharField("邮箱",max_length=100,null=True)
    code = models.CharField("验证码",max_length=100,null=True)
    send_type = models.CharField("发送类型",max_length=100,null=True)
    create_date = models.DateField("发送时间",auto_now_add=True,null=True)
    is_fail = models.CharField("是否失效：0 不失效、1 失效",max_length=10,default="0",null=True)

    class Mata:
        db_table = "EmailVerify"

    def __str__(self): # __unicode__ on Python 2
        return self.email

class Emailsports(models.Model):
    email = models.CharField("邮箱",max_length=100,null=True) 
    emailsporttitle = models.CharField("邮件活动题目",max_length=100,null=True)
    emailsportcontent =models.TextField("邮件活动内容",null=True,blank=True)
    emailsportlink = models.CharField("邮件活动链接",max_length=100,null=True) 
    create_date = models.DateField("发送时间",auto_now_add=True,null=True)
    is_fail = models.CharField("是否失效：0 不失效、1 失效",max_length=10,default="0",null=True) 

    class Mata:
        db_table = "Emailsports"

    def __str__(self): # __unicode__ on Python 2
        return self.email

class games(models.Model):
    gamesnumber = models.CharField("游戏id",max_length=300,null=True,blank=True)
    gamesname = models.CharField("游戏名字",max_length=300,null=True,blank=True)
    gamesinfo = models.TextField("游戏简介",null=True,blank=True)
    gamestype = models.CharField("游戏类别",max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "games"

    def __str__(self): # __unicode__ on Python 2
        return self.gamesname
class gamesinfo(models.Model):
    gamesnumber = models.CharField("游戏id",max_length=300,null=True,blank=True)
    gamesquestion = models.TextField("游戏问题",null=True,blank=True)
    gamesanswer = models.CharField("游戏答案",max_length=300,null=True,blank=True)
    gamesstatus = models.CharField("游戏状态：-1，0，1，2...",max_length=300,null=True,blank=True)
    createtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updatetime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    isfail = models.CharField(max_length=2,null=True,blank=True)    
    failtime = models.DateTimeField(auto_now_add=True,null=True,blank=True)
 
    class Mata:
        db_table = "gamesinfo"

    def __str__(self): # __unicode__ on Python 2
        return self.gamesnumber