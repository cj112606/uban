# -*- coding: utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,Http404
#from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.http import FileResponse 

from django.views.decorators import csrf
import os
from home.models import gamesinfo,games,EmailVerify,staff,staffinfo,sportlist,sport_request,sport_staff_request,requestlist,deptment,userVisitInfo
from django.utils.timezone import now, timedelta
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
import datetime  
from django.db.models import Avg, Max, Min,Count
from django.http import JsonResponse
from django.db import connection
import xlwt
from django.db.models import Q
from home import Checkcode
from home import email_yanzheng
from django.http import HttpResponse
from io import StringIO
import json
import io


def getIP(request,user_visit_form):  
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    #user_visit_ip = "1" 
    try:
        user_visit_ip = request.META['HTTP_X_FORWARDED_FOR'] 
    except KeyError:
        try:
            user_visit_ip = request.META['HTTP_X_REAL_IP'] 
        except KeyError:
            user_visit_ip = request.META.get('REMOTE_ADDR', None)
    user_visit_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    user_visit_cookies=request.COOKIES
    if user_visit_cookies:
        user_visit_cookies=request.COOKIES
        #print("COOKIES有值")
    else:
        user_visit_cookies=0
        #print("COOKIES为空！")
        #print(user_visit_cookies)        
    user_visit_terminal_type=request.environ['HTTP_ACCEPT'] 
    user_visit_date = time
    userVisitInfo.objects.create(user_visit_ip=user_visit_ip,user_visit_cookies=user_visit_cookies,user_visit_terminal_type=user_visit_terminal_type,user_visit_date=time,user_visit_form=user_visit_form,isfail="0")
    #print("IP:",user_visit_ip)
    return 0

def index(request):
    print("首页") 
    #getIP(request,"index")
    
    return render(request, 'index.html', locals())
    #return render(request, 'login.html', locals())
def newsin(request):
    print("新闻页面") 
    #getIP(request,"index") 
    
    return render(request, 'news.html', locals()) 
def couponsin(request):
    print("优惠券页面") 
    #getIP(request,"index") 
    
    return render(request, 'coupons.html', locals()) 
def vediosin(request):
    print("影视页面") 
    #getIP(request,"index") 
    
    return render(request, 'vedios.html', locals()) 
def gamesin(request):
    print("游戏页面") 
    #getIP(request,"index") 
    gameslists = games.objects.filter(isfail='1').order_by('gamesnumber').distinct('gamesnumber','gamesname')
    print(gameslists.query)
    return render(request, 'games.html', locals()) 

def gameschangein(request,changeid):
    print("游戏选择页面") 
    print(changeid)
    gcid = changeid
    gameslists = games.objects.filter(isfail='1').order_by('gamesnumber').distinct('gamesnumber','gamesname')
    gamesinfolists = games.objects.filter(gamesnumber=changeid) 
    print(gamesinfolists.query)
    #游戏简介，在数据库获取
    #gamesinfo="测试你对世界国家首都的认知，通过这游戏亦能进一步认识多些国家和首都名称。每次游戏随机出10个国家,作答时间为3秒。"
    #getIP(request,"index")  
    return render(request, 'gameschange.html', locals()) 

def gameschangeinfoin(request,changeid):
    print("游戏开始页面") 
    print(changeid)
    #游戏名称
    #gamesname='猜首都'
    #gamesinfo='国家名字'
    gameslists = games.objects.filter(isfail='1').order_by('gamesnumber').distinct('gamesnumber','gamesname')
    gameschangeid =changeid
    gamesinfolist = gamesinfo.objects.filter(gamesnumber=changeid)[0:1]

    #getIP(request,"index")  
    return render(request, 'gameschangeinfo.html', locals()) 

def gamesinfostartin(request,changeid):
    print("游戏开始页面执行") 
    print(changeid) 
    gameschangeid = changeid
    gamesinfolists = list(gamesinfo.objects.filter(gamesnumber=changeid).values_list("gamesnumber","gamesquestion","gamesanswer"))
    #getIP(request,"index")  
    return JsonResponse(gamesinfolists,safe=False) 

def gameschangeendin(request,changeid):
    print("游戏结束页面") 
    gameschangeid = changeid
    gameslists = games.objects.filter(isfail='1').order_by('gamesnumber').distinct('gamesnumber','gamesname')
    return render(request, 'gameschangeend.html', locals()) 


def sportconfirmin(request,sid):
    print("活动确认") 
    print(sid) 
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    print(staff_name)
    print(staff_id)
    sportnumber = sid
    staff_class = request.session.get('staff_class','0')
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login') 
    #查询活动员工报名表
    query="select a.requestname ,b.sport_staff_request_info from home_sport_staff_request b left join  home_requestlist a on a.requestnumber = b.requestnumber  where  b.staffnumber ='"+str(staff_id)+"' and b.sportnumber ='"+str(sportnumber)+"' and a.isfail = '0' "
    print(query)
    with connection.cursor() as c:
        try:
            c.execute(query)
            sport_staff_requestlists = c.fetchall()
            #for spl in staff_sport_lists:
              #print(spl[0])
              #print(spl[1])
              #print(spl[2])
              #print(spl[3])
              #print(spl[4])
        finally:
            c.close() 

    return render(request, 'sportconfirm.html', locals())
def updatesportstaffinfoin(request,sid):
    print("修改活动中员工信息") 
    print(sid) 
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    print(staff_name)
    print(staff_id)
    sportnumber = sid
    staff_class = request.session.get('staff_class','0')
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')
    return render(request, 'sportconfirm.html', locals())

def confirmtruein(request,sid):
    print("确认参加活动") 
    print(sid) 
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    print(staff_name)
    print(staff_id)
    sportnumber = sid
    staff_class = request.session.get('staff_class','0')
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')
    if request.POST:
        sport_staff_request.objects.filter(sportnumber=sportnumber,staffnumber=staff_id,isfail='0').update(updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
        sport_staff_request.objects.filter(sportnumber=sportnumber,staffnumber=staff_id,isfail='0').update(failtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
        sport_staff_request.objects.filter(sportnumber=sportnumber,staffnumber=staff_id,isfail='0').update(isfail = '2')
        if staff_class >'3':
            return HttpResponseRedirect('/staffinfoadmin') 
        else:
            return HttpResponseRedirect('/staffinfo') 
    return render(request, 'sportconfirm.html', locals())


def absentreasonin(request,sid):
    print("缺席原因") 
    print(sid) 
    sportnumber = sid
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(staff_name)
    print(staff_id)
    print(staff_class) 
    sportnumber=sid
        
    if staff_id == '0':
        print("staff_id")
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        print("staff_class")
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')
    if request.POST:
        a_reason = request.POST.get('a_reason')
        if a_reason.strip():
            print("更新数据")
            '''
            #obj = sport_staff_request.objects.get(sportnumber=sportnumber,staffnumber=staff_id,isfail='0')
            sport_staff_request.objects.filter(sportnumber=sportnumber,staffnumber=staff_id,isfail='0').update(updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
            sport_staff_request.objects.filter(sportnumber=sportnumber,staffnumber=staff_id,isfail='0').update(failtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
            sport_staff_request.objects.filter(sportnumber=sportnumber,staffnumber=staff_id,isfail='0').update(failreason = a_reason.strip())
            sport_staff_request.objects.filter(sportnumber=sportnumber,staffnumber=staff_id,isfail='0').update(updatetime = isfail = '-1')
            '''
            '''
            obj = sport_staff_request.objects.get(sportnumber=sportnumber)  
            obj.updatetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
            obj.isfail = '-1'
            obj.failreason = a_reason.strip()
            obj.failtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
            print(obj)
            #obj.save()
            '''
            return HttpResponseRedirect('/staffinfo') 
        else:
            errreasonlist="缺席原因不能为空"
            return render(request, 'absentreason.html', locals())

    return render(request, 'absentreason.html', locals())

def staffinfoin(request):
    print("个人信息") 
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(staff_id)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login') 
    if staff_class >='3':
        return HttpResponseRedirect('/staffinfoadmin') 
    print(staff_name)
    print(staff_id)
    staffinfoLists = staffinfo.objects.filter(isfail="0",staffnumber=staff_id)[0:1]
    sportLists = sportlist.objects.filter(isfail="0")[0:5]
    query="select a.sportname,a.sportcontent,a.sportlink,to_date(to_char(b.createtime,'yyyy-mm-dd'),'yyyy-mm-dd') soprtcreatetime, case  when b.isfail::numeric < 0 then '不参加活动'  when  b.isfail::numeric > 0 then '已确认参加'  when  b.isfail::numeric = 0 then '待确认参加活动' end sport_join_status,c.bz from home_sportlist a  join home_sport_staff_request b   on a.sportnumber = b.sportnumber left join home_staffinfo c on b.staffnumber=c.staffnumber where  b.staffnumber ='"+str(staff_id)+"' group by a.sportname,a.sportcontent,a.sportlink,to_date(to_char(b.createtime,'yyyy-mm-dd'),'yyyy-mm-dd'),case  when b.isfail::numeric < 0 then '不参加活动' when  b.isfail::numeric > 0 then '已确认参加' when  b.isfail::numeric = 0 then '待确认参加活动' end,c.bz  order by to_date(to_char(b.createtime,'yyyy-mm-dd'),'yyyy-mm-dd')"
    print("------------query----------------")
    print(query)
    print("------------query----------------")
    with connection.cursor() as c:
        try:
            c.execute(query)
            staff_sport_lists = c.fetchall()            
            #for spl in staff_sport_lists:
              #print(spl[0])
              #print(spl[1])
              #print(spl[2])
              #print(spl[3])
              #print(spl[4])
        finally:
            c.close() 
    return render(request, 'staffinfo.html', locals())

def staffinfoadmin(request):
    print("管理员信息")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(staff_name)
    print(staff_id)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class < '3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')     
    sportLists = sportlist.objects.filter(isfail="0")
    staffinfoLists = staffinfo.objects.filter(isfail="0",staffnumber=staff_id)[0:1]
    sportselfLists = sportlist.objects.filter(isfail="0",sportauthor=staff_name)[0:5] 
    query="select a.sportname,a.sportcontent,a.sportlink,to_date(to_char(b.createtime,'yyyy-mm-dd'),'yyyy-mm-dd') soprtcreatetime, case  when b.isfail::numeric < 0 then '不参加活动'  when  b.isfail::numeric > 0 then '已确认参加'  when  b.isfail::numeric = 0 then '待确认参加活动' end sport_join_status from home_sportlist a  join home_sport_staff_request b   on a.sportnumber = b.sportnumber where  b.staffnumber ='"+str(staff_id)+"' group by a.sportname,a.sportcontent,a.sportlink,to_date(to_char(b.createtime,'yyyy-mm-dd'),'yyyy-mm-dd'),case  when b.isfail::numeric < 0 then '不参加活动' when  b.isfail::numeric > 0 then '已确认参加' when  b.isfail::numeric = 0 then '待确认参加活动' end  order by to_date(to_char(b.createtime,'yyyy-mm-dd'),'yyyy-mm-dd')"
    with connection.cursor() as c:
        try:
            c.execute(query)
            staff_sport_lists = c.fetchall()
            #for spl in staff_sport_lists:
              #print(spl[0])
              #print(spl[1])
              #print(spl[2])
              #print(spl[3])
              #print(spl[4])
        finally:
            c.close()
    

    '''
    query = "select c.flowers_id,c.flowers_name,count(id) from deathstar_jidianers_flowers_stars c where is_fail = '0' and c.name='" + user_name + "' and c.jidianers_id = "+str(user_id)+"::numeric group by  c.flowers_id,c.flowers_name"
    #query = "select a.id,a.name,b.stars_id,b.stars_name,c.stars_id,c.stars_name,c.flowers_id,c.flowers_name,count(b.jidianers_id) AS likeNums,count(c.jidianers_id) AS flowerNums  from deathstar_jidianers  as a left join (select * from deathstar_jidianers_like_stars  where is_fail = '0') b on a.id=b.jidianers_id left join (select * from  deathstar_jidianers_flowers_stars where is_fail = '0') c on a.id=c.jidianers_id  where a.is_fail = '0' and a.jidianers_class >='1'    group by  a.id,a.name,b.stars_id,b.stars_name,c.stars_id,c.stars_name,c.flowers_id,c.flowers_name order by c.stars_id"
    #starsList = stars.objects.raw(query)
    with connection.cursor() as c:
        try:
            c.execute(query)
            flowerstarsList = c.fetchall()
            #for sl in flowerstarsList:
            #   print(sl[0])
            #   print(sl[9])
        finally:
            c.close()
    '''
    return render(request, 'staffinfoadmin.html', locals())
def login(request):
    print("登录") 
    if request.POST: 
        i_staffname =request.POST['uname'].strip() 
        i_staffpw  = request.POST.get('pwords')
        #name = 'xiaoyu'
        #password = '123'
        '''
        print(i_staffname.strip())
        print(i_staffpw.strip())
        i_staffname 为18位 就是身份证
        i_staffname为11为就是手机号
        i_staffname带@就是邮箱
        其余的是oa
        '''
        if '@' in i_staffname.strip():
            staffinfosList = staffinfo.objects.filter(isfail=0,staffemail__iexact=i_staffname.strip().upper(),staffpw__iexact=i_staffpw.strip().upper())
        elif len(i_staffname.strip())==18:
            #i_staffname 为18位 就是身份证
            staffinfosList = staffinfo.objects.filter(isfail=0,staffidcard__iexact=i_staffname.strip().upper(),staffpw__iexact=i_staffpw.strip().upper())
        elif len(i_staffname.strip())==11:
            staffinfosList = staffinfo.objects.filter(isfail=0,staffphone__iexact=i_staffname.strip().upper(),staffpw__iexact=i_staffpw.strip().upper())
        else:
            staffinfosList = staffinfo.objects.filter(isfail=0,staffoaccount__iexact=i_staffname.strip().upper(),staffpw__iexact=i_staffpw.strip().upper())
        #staffinfosList = staffinfo.objects.filter(isfail=0,staffname__iexact=i_staffname.upper(),staffpw__iexact=i_staffpw.upper())
        print(staffinfosList)
        if staffinfosList:
            for v_staffinfo in staffinfosList:
                if v_staffinfo.staffclass <= '0':
                    #print("您曾经有违规操作，该用户已经锁定，请联系管理员解锁！")
                    errloggin = "您曾经有违规操作，该用户已经锁定，请联系管理员解锁！"
                    request.session["is_succ"]='-1'
                    request.session["staff_name"] = '游客'
                    request.session["staff_id"] = '0'
                    return render(request, 'login.html', locals())
                elif v_staffinfo.staffclass >='3':
                    request.session["staff_name"] = v_staffinfo.staffname
                    request.session["staff_id"] = v_staffinfo.staffnumber
                    request.session["staff_class"] = v_staffinfo.staffclass
                    staff_name = request.session.get('staff_name','游客')
                    staff_id = request.session.get('staff_id','0')
                    staff_class = request.session.get('staff_class','0')
                    print("登录成功！")
                    request.session["is_succ"]='1'
                    return HttpResponseRedirect('/staffinfoadmin')
                    #return render(request, 'staffinfoadmin.html', locals())
                else:                    
                    request.session["staff_name"] = v_staffinfo.staffname
                    request.session["staff_id"] = v_staffinfo.staffnumber
                    request.session["staff_class"] = v_staffinfo.staffclass
                    staff_name = request.session.get('staff_name','游客')
                    staff_id = request.session.get('staff_id','0')
                    print("登录成功！")
                    request.session["is_succ"]='1'
                    return HttpResponseRedirect('/staffinfo')
                    #return render(request, 'staffinfo.html', locals())
        else:
            request.session["staff_name"] = '游客'
            request.session["staff_id"] = '0'
            print("用户名密码错误！！！")
            request.session["is_succ"]='0'
            errloggin = "用户名密码错误！！！"
            return render(request,'login.html',locals()) 
    return render(request, 'login.html', locals())

def logout(request):
    print("logout")
    staff_name = request.session.get('staff_name','游客')
    if staff_name == '游客':
        return render(request,'login.html',locals())
    else:
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
    return render(request,'login.html',locals()) 
def addrequestattrin(request):
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    print("添加属性") 
    i_attrtname =request.GET['staffattr'] 
    if i_attrtname:
        #print(i_attrtname)
        v_id=requestlist.objects.aggregate(Max('id'))
        id=int(v_id['id__max'])+1 
        v_requestnumber=requestlist.objects.aggregate(Max('requestnumber'))
        i_requestnumber=int(v_requestnumber['requestnumber__max'])+1 
        is_top = 1 
        toptime = time
        topcycle = 24
        isfail = 0
        createtime = time
        updatetime = time
        '''
        print(i_requestnumber)
        print(is_top)
        print(toptime)
        print(topcycle)
        print(isfail)
        print(createtime)
        print(updatetime)
        '''
        requestattrs_lists = list(requestlist.objects.filter(requestname=i_attrtname,isfail=0).values_list("requestname"))
        print(requestattrs_lists)
        if requestattrs_lists:
            print("属性已经存在！！！")
            successattrtname ="添加属性失败!!!属性已经存在！！！"
            requestlist_lists =[]
            requestlist_lists.append(successattrtname)            
        else:
            #添加属性到表中
            print("属性添加成功！")
            requestlist.objects.create(id=id,requestnumber=i_requestnumber,requestname=i_attrtname,createtime=createtime,updatetime=updatetime,is_top=is_top,toptime=toptime,topcycle=topcycle,isfail=isfail)
            requestlist_lists = list(requestlist.objects.filter(isfail=0).values_list("requestnumber","requestname"))
            #requestlist_lists.append("hueys")        
            #print(type(requestlist_lists))
            

    else:
        print("属性输入为空！！！")
        successattrtname ="添加属性失败!!!属性输入为空，请添加属性值."
        requestlist_lists =[]
        requestlist_lists.append(successattrtname)
        #属性输入为空，请他重新输入
    return JsonResponse(requestlist_lists,safe=False) 
 
def createsportin(request):
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login') 
    if staff_class <'3':
            del request.session['staff_name']  #删除session
            del request.session['staff_id']  #删除session
            del request.session['staff_class']  #删除session
            return HttpResponseRedirect('/login')      
    print("创建活动")
    getIP(request,"createsportin")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    requestlists=requestlist.objects.filter(isfail=0).order_by("-updatetime")
    #i_sportname =request.POST['Sportname']
    #i_sportcontent =request.POST['Sportcontent']
    print(staff_name)
    print("----------")
    print(request)
    if request.POST:  
        print("创建活动11")
        #i_sportnumber =request.POST['Sportnumber']
        id=sportlist.objects.aggregate(Max('sportnumber'))
        i_sportnumber=int(id['sportnumber__max'])+1
        #i_sportnumber=1
        i_sportname =request.POST['Sportname']
        i_sportcontent =request.POST['Sportcontent']
        i_sportlink = i_sportnumber

        sportstartdate =request.POST['sportstarttime']
        sportenddate =request.POST['sportendtime']
        sporttype =request.POST['sporttype']
        print('--------i_sportstarttime-----------')
        print(sportstartdate)
        print(sportenddate)
        print(sporttype) 
        print('--------i_sportstarttime-----------') 

        is_top = 1 
        toptime = time
        topcycle = 24
        isfail = 0
        createtime = time
        updatetime = time
        now = datetime.datetime.now()
        #sportstartdate = now + datetime.timedelta(days=15)
        #sportenddate = now + datetime.timedelta(days=60)
        sportauthor =staff_name 
        request_lists = request.POST.getlist('check_box_list')        
        if request_lists: 
            print(request_lists)
            '''                
            sportlist.objects.create(
                sportnumber=i_sportnumber,sportname=i_sportname,
                sportcontent=i_sportcontent,sportlink=i_sportlink,
                sportauthor=sportauthor, 
                sportstartdate=sportstartdate,sportenddate=sportenddate,
                sporttype=sporttype, 
                is_top=is_top,toptime=toptime,topcycle=topcycle,
                isfail=isfail,createtime=createtime,updatetime=updatetime)
            for request_attr in request_lists:
                print(request_attr)
                sport_request.objects.create(
                sportnumber=i_sportnumber,
                requestnumber =request_attr 
                ,createtime=createtime,updatetime=updatetime, isfail=isfail)
                #errlist = errlist + str(request_attr)+ " "
            '''
            successfullist ='选择了额外属性创建活动成功！！！ ' 
            print(successfullist)             
        else:
            '''
            sportlist.objects.create(
                sportnumber=i_sportnumber,sportname=i_sportname,
                sportcontent=i_sportcontent,sportlink=i_sportlink,
                sportauthor=sportauthor,
                sportstartdate=sportstartdate,sportenddate=sportenddate,
                sporttype=sporttype,
                is_top=is_top,toptime=toptime,topcycle=topcycle,
                isfail=isfail,createtime=createtime,updatetime=updatetime) 

            sport_request.objects.create(sportnumber=i_sportnumber,createtime=createtime,updatetime=updatetime, isfail=isfail)
            '''
            successfullist = '选择默认属性创建活动成功！！！ '
            print(successfullist)   
        staffLists = staffinfo.objects.filter(~Q(staffemail=''),staffname="陈剑",isfail=0,staffclass__gte="1") 
        return render(request, 'successfulcreatesport.html', locals())
    print(staff_name)
    return render(request, 'createsport.html', locals())

def sendEmailsportsin(request):
    print("发送邮件")
    staff_email_num = 0
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login') 
    if staff_class <'3':
            del request.session['staff_name']  #删除session
            del request.session['staff_id']  #删除session
            del request.session['staff_class']  #删除session
            return HttpResponseRedirect('/login')         
    if request.POST:
        #获取活动名字和内容以及连接
        i_sportname = request.POST['i_sportname']
        i_sportlink = request.POST['i_sportlink']
        i_sportcontent = request.POST['sportcontent'] 
        staff_email_lists = request.POST.getlist('staff_email_list')
        for staff_email  in staff_email_lists:
            print("-----------staff_email----------")
            print(staff_email)
            sporttitle=i_sportname
            sportcontent=i_sportcontent
            sportlink=i_sportlink
            sportlink="http://127.0.0.1:8000/injoinsport/" + str(i_sportlink) +"/"
            print(sporttitle)
            print(sportcontent)
            print(sportlink)

            print("-----------staff_email----------")
            if 'all' in staff_email:
                print("给所有员工发送")
                #staffinfoLists = staffinfo.objects.filter(~Q(staffemail=''),isfail=0,staffclass__gte="1")
                staffinfoLists = staffinfo.objects.filter(~Q(staffemail=''),staffname="陈剑",isfail=0,staffclass__gte="1")  
                for staffinfos in staffinfoLists:                   
                    print("-----------staffinfos----------")
                    #print(type(staffinfos))
                    print(staffinfos.staffemail)
                    sendEmailNum = email_yanzheng.send_sportcontent_email(staffinfos.staffemail,sporttitle,sportcontent,sportlink)
                    staff_email_num = staff_email_num + 1
                    print("-----------staffinfos----------")
                break
            else:   
                #sendmailresult = "活动"
                email=staff_email
                sendEmailNum = email_yanzheng.send_sportcontent_email(email,sporttitle,sportcontent,sportlink)
                staff_email_num = staff_email_num + sendEmailNum
                print(staff_email_num) 
    return render(request,'successfulsendmail.html',locals())




def searchsportin(request,id):
    print("查看活动")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    sport_lists = list(sportlist.objects.filter(sportlink=id,isfail=0).values_list("sportnumber","sportname","sportcontent"))
    #sport_lists =  sportlist.objects.filter(sportlink=id,isfail=0).values_list("sportnumber","sportname","sportcontent")
    if sport_lists:
        sport_re = '查看活动成功' 
    else:
        sport_re = '没有找到活动'
    return JsonResponse(sport_lists,safe=False) 
    #return render(request, 'index.html', locals())

def checkdepartmentin(request):
    print("查看部门")    
    if request.POST:
        sport_id = request.POST['Sport_id']
        #print(sport_id)
        i_username = request.POST['Username']
        if i_username:
            #print(i_username)
            #staff_lists =  staff.objects.filter(staffname=i_username,isfail=0).order_by("-updatetime")[0:1]
            cursor = connection.cursor()
            sql = "select * from home_staff a where a.isfail = '0' and a.staffname='" + str(i_username)+"' limit 2" 
            print(sql)
            cursor.execute(sql) 
            staff_lists = cursor.fetchall()
            print(staff_lists)
            #sport_lists = list(sportlist.objects.filter(sportnumber=sport_id,isfail=0).order_by("-updatetime")[0:1])
            sql = "select a.sportnumber,a.sportname,a.sportcontent from home_sportlist a  where a.isfail = '0' and a.isfail = '0' and a.sportnumber='" + str(sport_id)+"'" 
            cursor.execute(sql) 
            sport_lists = cursor.fetchall()
            sql = "select b.requestnumber,b.requestname from home_requestlist b  left join home_sport_request a  on a.requestnumber = b.requestnumber where a.isfail = '0' and b.isfail = '0' and a.sportnumber='" + str(sport_id)+"'" 
            cursor.execute(sql) 
            sport_request_lists = cursor.fetchall()
            print(sport_request_lists)
            cursor.close()
            #return render(request, 'joinsport.html', locals())
            #return JsonResponse(sport_lists,safe=False) 
            return JsonResponse({"sport_request_lists":sport_request_lists,"i_username":i_username,"staff_lists":staff_lists,"sport_lists":sport_lists},safe=False)
        else:
            errlist = '未查到部门，请重新输入'
    return render(request, 'errUsername.html', locals())
    #return render(request, 'joinsport.html', locals())

def joinsportin(request,id):
    getIP(request,"joinsportin")
    print("查看活动需求")
    sport_id = id
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    #sport_lists =  list(sportlist.objects.filter(sportlink=id,isfail=0).values_list("sportnumber","sportname","sportcontent"))
    sport_lists =  sportlist.objects.filter(sportlink=id,isfail=0).order_by("-updatetime")[0:1]
    #(sportnumber=id,isfail=0)
    cursor = connection.cursor()
    sql = "select b.requestnumber,b.requestname from home_requestlist b  left join home_sport_request a  on a.requestnumber = b.requestnumber where a.isfail = '0' and b.isfail = '0' and a.sportnumber='" + str(id)+"'" 
    print(sql)
    cursor.execute(sql) 
    sport_request_lists = cursor.fetchall()
    print(sport_request_lists)
    cursor.close()
    if sport_lists:
        sport_re = '查看活动成功' 
    else:
        sport_re = '没有找到活动'
    print(sport_re)
    if request.POST:
        #sport_id = request.POST['Sport_id']
       
        print(sport_lists)
        #sport_id = id
        #print(sport_id)
        i_username = request.POST['Username']
        if i_username:
            print("参加活动，根据姓名返回单位、部门、性别")
            #print(i_username)
            #staff_lists =  staff.objects.filter(staffname=i_username,isfail=0).order_by("-updatetime")[0:1]
            cursor = connection.cursor()
            sql = "select staffnumber,staffname,staffdept,staffunit,staffsex from home_staff a where a.isfail = '0' and a.staffname like '" + str(i_username)+"%' limit 2" 
            #print(sql)
            cursor.execute(sql) 
            staff_lists = cursor.fetchall()
            #print(staff_lists)
            cursor.close()
            cursor = connection.cursor()
            #sport_lists = list(sportlist.objects.filter(sportnumber=sport_id,isfail=0).order_by("-updatetime")[0:1]
            sql = "select b.requestnumber,b.requestname from home_requestlist b  left join home_sport_request a  on a.requestnumber = b.requestnumber where a.isfail = '0' and b.isfail = '0' and a.sportnumber='" + str(sport_id)+"'" 
            cursor.execute(sql) 
            sport_request_lists = cursor.fetchall()
            print(sport_request_lists)
            cursor.close()
            return render(request, 'joinsport.html', locals())
            #return JsonResponse(sport_lists,safe=False) 
            #return JsonResponse({"sport_request_lists":sport_request_lists,"i_username":i_username,"staff_lists":staff_lists,"sport_lists":sport_lists},safe=False)
        else:
            errlist = '未查到部门，请重新输入'
    return render(request, 'joinsport.html', locals())

def insertsportin(request):
    print("插入活动表")
    getIP(request,"insertsportin")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    if request.POST:
        #print(request.POST)
        i_username =request.POST['Username']
        i_usernumber =request.POST['UserNumber']
        sport_id =request.POST['Sportid']
        deptcheck =request.POST['deptcheck']
        print("deptcheck")
        print(deptcheck)
        i_username = deptcheck
        i_sportname = list(sportlist.objects.filter(sportnumber=sport_id,isfail=0).order_by("-updatetime")[0:1])[0]
        print(i_sportname)
        i_unit =request.POST['Unit']
        i_dept=request.POST['Dept']
        i_sex=request.POST['Sex']
       
        if i_username:
            result_infos = {"单位":i_unit, "部门":i_dept,"性别":i_sex} 
            #print(result_infos)
            #sport_staff_request.objects.create(sportnumber=sport_id,staffnumber=i_usernumber,requestnumber="部门", sport_staff_request_info=i_dept ,createtime=time,updatetime=time,isfail='0')
            #sport_staff_request.objects.create(sportnumber=sport_id,staffnumber=i_usernumber,requestnumber="性别", sport_staff_request_info=i_sex ,createtime=time,updatetime=time,isfail='0')
            #sport_staff_request.objects.create(sportnumber=sport_id,staffnumber=i_usernumber,requestnumber="单位", sport_staff_request_info=i_unit ,createtime=time,updatetime=time,isfail='0')
            cursor = connection.cursor()
            sql = "select a.requestnumber,b.requestname,a.sportnumber from home_sport_request a left join home_requestlist b on a.requestnumber =b.requestnumber where a.isfail = '0' and a.sportnumber='" + str(sport_id)+"'" 
            #print(sql)
            cursor.execute(sql) 
            sport_request_lists = cursor.fetchall()           
            print(sport_request_lists) 
            print("---------sql1------------") 
            sql1 = "select b.requestname,a.sport_staff_request_info,a.updatetime from home_sport_staff_request a left join home_requestlist b  on a.requestnumber =b.requestnumber  where a.isfail >= '0' and a.sportnumber='" + str(sport_id)+"'and a.staffnumber='" + str(deptcheck)+"'" 
            print(sql1)
            print("---------------------") 
            cursor.execute(sql1) 
            is_signup_lists = cursor.fetchall()
            #is_signup_lists = sport_staff_request.objects.filter(sportnumber=sport_id,staffnumber=i_usernumber)[0:1]   
            print(deptcheck)
            cursor = connection.cursor()
            sql = "select * from home_staff a where a.isfail = '0' and a.staffnumber = '" + str(deptcheck)+"' limit 2" 
            print(sql)
            cursor.execute(sql) 
            staffdept_lists = cursor.fetchall()
            print("--------------------")
            print("staffdept_lists")
            print(staffdept_lists)
            print("--------------------") 
            for staffdepts in staffdept_lists:
                i_usernumber = staffdepts[1]
                i_username = staffdepts[2]
                i_unit = staffdepts[5] 
                i_dept =staffdepts[6] 
                i_sex = staffdepts[7] 
            print(i_usernumber,i_username,i_unit,i_dept,i_sex) 
            print("--------------------")
            if is_signup_lists:
                print("报名失败，您已经报名过了！")
                successful_result = "报名失败!!!" + str(i_username) + '您已经报名过了！报名信息如下：'
                #successful_result = str(i_sportname) + ' 活动，'+ str(i_username) + '您已经报名过了！报名信息如下：'
                for  signupinfo in is_signup_lists:
                    print(signupinfo[1])
                    print(signupinfo[0])
                    print(signupinfo[2])
                    result_infos[signupinfo[0]]  =  signupinfo[1]
                    #requestnumber,sport_staff_request_info
                return render(request, 'errsignupfail.html', locals())
            else:
                for sport_requests in sport_request_lists:
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                    #print(sport_requests)
                    #print(sport_requests[0])
                    #print(sport_requests[1])
                    #print(request.POST[sport_requests[0]])
                    #print(request.POST[sport_requests[0]])
                    requestnumber=sport_requests[0]
                    isfail='0'
                    print("--------sport_staff_request.objects.create---------")                    
                    print(i_usernumber,sport_id,sport_requests[2],sport_requests[0],request.POST[sport_requests[0]],isfail)
                    sport_staff_request.objects.create(sportnumber=sport_id,staffnumber=i_usernumber,requestnumber=sport_requests[0], sport_staff_request_info=request.POST[sport_requests[0]],createtime=time,updatetime=time,isfail='0')
                    #print(requestname) 
                    print("--------sport_staff_request.objects.create---------")
                    result_infos[sport_requests[1]]  =  request.POST[sport_requests[0]]
                    print(result_infos)
                #successful_result = '恭喜您，'+str(i_sportname)+' 活动提交成功'
                #查看活动返回
                return render(request, 'successfulsport.html', locals())
        else:
            errlist = '请先填写姓名'
            return render(request, 'errUsername.html', locals())
    return render(request, 'joinsportin.html', locals())

    
def insearchsportsin(request):
    print("查看活动id")
    taff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0') 
    print(request.GET)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')  
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    if request.POST:       
        searchsport =request.POST['q']
        sport_lists =  sportlist.objects.filter(sportname__contains=searchsport,isfail=0).order_by("-updatetime")
        if sport_lists: 
            sport_re = '查看活动成功' 
        else:
            sport_re = '没有找到活动'
        deptmentlists = deptment.objects.filter(isfail=0).order_by("-updatetime")
        return render(request, 'expsportinfo.html', locals())
    return render(request, 'expsportinfo.html', locals())
    

def staffsearchsportsin(request):
    print("员工或者管理员查看活动id")
    sport_rec = 'staff'
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(request.GET)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')  
    if staff_class >='3': 
        sport_rec = 'admin'
    print(sport_rec)
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    if request.GET:
        print("---------searchsport--------")
        searchsport =request.GET['q']
        print(searchsport)
        print("---------searchsport--------")
        #sport_lists =  sportlist.objects.filter(sportname__contains=searchsport,isfail=0).order_by("-updatetime")
        searchsportsql  = "select a.sportnumber,a.sportname,a.sportcontent,a.sportlink,a.sportauthor, a.sportstartdate,a.sportenddate,replace(a.sporttype,'|',' ') ,a.isfail ,count(distinct b.staffnumber) hot from (select * from home_sportlist a where upper(a.sportname) like upper('%" + str(searchsport)+"%' )) a left join (select * from home_sport_staff_request b where b.isfail >= '0' ) b on a.sportnumber =b.sportnumber group by a.sportnumber,a.sportname,a.sportcontent,a.sportlink,a.sportauthor, a.sportstartdate,a.sportenddate,replace(a.sporttype,'|',' '),a.isfail " 
        print(searchsportsql)
        print("---------searchsportsql------------") 
        cursor = connection.cursor()
        cursor.execute(searchsportsql) 
        sport_lists = cursor.fetchall()
        for sportinfo in sport_lists:
                print(sportinfo[0])
                print(sportinfo[1])
                print(sportinfo[2])
                print(sportinfo[3])
                print(sportinfo[4])
                print(sportinfo[5])
                print(sportinfo[6]) 
                print(sportinfo[7]) 
                print(sportinfo[8]) 
                print(sportinfo[9]) 
                #print(sportinfo[10])  
        print("---------res------------") 
        '''
        ''' 
        return render(request, 'searchsports.html', locals())
    return render(request, 'searchsports.html', locals())


def expsportinfoin(request):
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(staff_id)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')     
    print("导出活动名单")
    succlist = {}
    download_file_lists = []
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    deptmentlists = deptment.objects.filter(isfail=0).order_by("-updatetime")            
    if request.POST:  
        search_sports_lists = request.POST.getlist('search_sports_list')
        if search_sports_lists:
            print("search_sports_lists：",search_sports_lists)
            deptnumber_lists = request.POST.getlist('check_box_list')
            #print("check_box_list")
            #print(deptnumber_lists)     
            if deptnumber_lists:
                for sports in search_sports_lists:                    
                    for deptnumber in deptnumber_lists:
                        print("deptnumber:",deptnumber)
                        cursor = connection.cursor()
                        #sportnumber = sports
                        sql = "select fun_create_sport_info('" + str(sports)+"','"+deptnumber+"')" 
                        print(sql)
                        cursor.execute(sql)

                        file=os.getcwd()+'\\static\\downfilepath\\' 
                        tablename ='tb_sport_info_'+deptnumber+'_'+ sports
                        write_data_to_excel(file,tablename) 
                        #succlist = "下载成功！文件目录： "+file+",文件名字： "+tablename+".xls"
                        download_file_lists.append(tablename)
                succlist = "文件生成成功！"                     
                sport_lists =  sportlist.objects.filter(sportnumber=sports,isfail=0).order_by("-updatetime")
                return render(request, 'expsportinfo.html', locals())
            else:
                errlist = '请选择需要导出名单的部门'
                return render(request, 'errdept.html', locals())
        else:
            errlist = '请选择需要导出的活动'
            return render(request, 'errdept.html', locals())
    return render(request, 'expsportinfo.html', locals())

def download_filein(request,deptnumber,sports):
    """
    sql 文件下载
    :param request:
    :return:
    """
    print("文件下载")
    filepath=os.getcwd()+'\\static\\downfilepath\\'     
    #filename ='tb_sport_info_'+deptnumber+'_'+ sports+'.xls' 
    filename =deptnumber+'_'+ sports+'.xls' 
    #print("filename:") 
    #print(filename) 
    download_file = (filepath+filename)
    #print(download_file)
    #download_file.replace('\\', '\')
    file=open(download_file,'rb')
    #print(file)  
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'  
    response['Content-Disposition']='attachment;filename='+filename  
    return response  
 

def write_data_to_excel(file,table_name):
    #result = get_data(host,user,passwd,db,sql)
    cursor = connection.cursor()
    sql = "select * from "+table_name
    cursor.execute(sql)     
    result = cursor.fetchall() 
    cursor.close()
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('sheet',cell_overwrite_ok=True)
    workbook = xlwt.Workbook(encoding='utf-8')
    cursor = connection.cursor()
    sql = "SELECT a.attnum, case when a.attname ='sportnumber' then '活动编号' when a.attname ='sportname' then '活动标题' when a.attname ='sportcontent' then '活动内容' when a.attname ='staffnumber' then '姓名序号' when a.attname ='staffname' then '姓名' when a.attname ='staffdept' then '部门' when a.attname ='staffunit' then '单位' when a.attname ='staffsex' then '性别' else a.attname end AS field FROM pg_class c, pg_attribute a LEFT OUTER JOIN pg_description b ON a.attrelid=b.objoid AND a.attnum = b.objsubid, pg_type t WHERE c.relname = '"+table_name+"' and a.attnum > 0 and a.attrelid = c.oid and a.atttypid = t.oid ORDER BY a.attnum;"
    cursor.execute(sql)     
    table_attname_results = list(cursor.fetchall())
    cursor.close()
    #print(table_attname_results)
    #第一行
    leng_i = 0
    for table_attname in table_attname_results:
        #print(table_attname[1])
        sheet.write(0, leng_i, table_attname[1])
        leng_i = leng_i+1
    leng_i = 1
    for i in range(len(result)):
        #对result的每个子元素作遍历，
        print('输出中...')
        for j in range(len(result[i])):
            #将每一行的每个元素按行号i,列号j,写入到excel中。
            sheet.write(leng_i,j,result[i][j])
            #print(result[i][j])
            print('..')
        leng_i = leng_i+1

    # 以传递的name+当前日期作为excel名称保存。
   
    filename = file+str(table_name)+'.xls'
    print(filename)
    wbk.save(filename) 

def forgetpasswin(request):
    print("忘记密码")
    if request.POST:
        print("1")
        i_forgetEmail =request.POST['forgetEmail']
        i_forgetIDcard =request.POST['forgetIDcard']
        i_forgetcord =request.POST['forgetcord']
        print("------forgetpasswin---------")
        print(i_forgetEmail)
        print(i_forgetIDcard)
        print(i_forgetcord)
        print("------forgetpasswin---------")
        is_staffinfoList=staffinfo.objects.filter(staffemail=i_forgetEmail,staffidcard=i_forgetIDcard).count()
        if  is_staffinfoList ==0:
            print("未找到email或者身份证")
            errforget = '未找到email或者身份证!!'
            return render(request, 'forgetpassw.html', locals())
        if i_forgetcord.upper()==request.session['checkcodforgetpassw'].upper():
            print("验证成功！") 
            email_yanzheng.send_uppassword_email(i_forgetEmail, "uppassword")
            return render(request,'forgetpasswyanz.html',locals())
            #return render(request,'getbackpassyanz.html',locals())
        else:             
            errforget = '验证码错误！'
    return render(request, 'forgetpassw.html', locals())
def forgetpasswyanzin(request):
    print("忘记密码验证")
    if request.POST:
        Yanz  = request.POST['forgetEmailyanz'] 
        i_forgetEmail =  request.POST['forgetEmail']
        print("---------i_forgetEmail-----------")
        print(i_forgetEmail)
        print("---------i_forgetEmail-----------")
        EmailVerifyList=EmailVerify.objects.filter(email=i_forgetEmail,send_type="uppassword").order_by('-id')[:1]
        for EmailVerifys in EmailVerifyList:
            v_code = str(EmailVerifys.code)
        if Yanz.upper()==v_code.upper():#邮件的验证码
            return render(request,'forgetpasswupdtepw.html',locals())
        else:
            errreyanz='验证码错误！'
            return render(request,'forgetpasswyanz.html',locals())
    return render(request,'forgetpasswyanz.html',locals())

def forgetpasswuppwin(request):
    print("密码重置")
    if request.POST:
        i_forgetEmail =  request.POST['forgetEmail']
        i_forgetpasswnew =  request.POST['forgetpasswnew']
        print("---------i_forgetpasswnew-----------")
        print(i_forgetEmail)
        print(i_forgetpasswnew)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        print("密码重置成功")
        print("---------i_forgetpasswnew-----------")
        staffinfo.objects.filter(staffemail=i_forgetEmail).update(updatetime = time)
        staffinfo.objects.filter(staffemail=i_forgetEmail).update(staffpw = i_forgetpasswnew)
        staffinfo.objects.filter(staffemail=i_forgetEmail).update(staffclass = '1')
        return render(request, 'forgetpasswupdtepwsuc.html', locals()) 
    return render(request, 'forgetpasswupdtepw.html', locals())

def checkEmailin(request):
    print("验证邮箱")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(staff_id)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login') 
    staffinfoLists = staffinfo.objects.filter(isfail="0",staffnumber=staff_id)[0:1] 
    if staffinfoLists:
        for staffinfos in staffinfoLists:
            i_checkEmail = staffinfos.staffemail
            print("-------i_checkEmail----")
            print(staffinfos.staffemail)
            print(i_checkEmail)
            print("-------i_checkEmail----")
            if i_checkEmail:
                i_checkEmail = i_checkEmail
            else:
                i_checkEmail = " "
        print("-------i_checkEmail----")
        print(staffinfos.staffemail)
        print(i_checkEmail)
    if request.POST:  
        i_checkEmail = request.POST['checkEmail'] 
        email_yanzheng.send_uppassword_email(i_checkEmail, "checkEmail")
        return render(request,'checkEmailyanz.html',locals()) 
    return render(request, 'checkEmail.html', locals())

def checkEmailyanzin(request):
    print("验证邮箱验证码验证")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(staff_id)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'0':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login') 
    if request.POST:
        Yanz  = request.POST['checkEmailyanz'] 
        i_checkEmail =  request.POST['checkEmail']  
        print("---------i_checkEmail-----------")
        print(i_checkEmail) 
        print("---------i_checkEmail-----------")
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        EmailVerifyList=EmailVerify.objects.filter(email=i_checkEmail,send_type="checkEmail").order_by('-id')[:1]
        for EmailVerifys in EmailVerifyList:
            v_code = str(EmailVerifys.code)
        if Yanz.upper()==v_code.upper():#邮件的验证码
            staffinfo.objects.filter(staffnumber=staff_id).update(updatetime = time) 
            staffinfo.objects.filter(staffnumber=staff_id).update(staffclass = '2')  
            return render(request,'checkEmailsucc.html',locals())
        else:
            errcheckyanz='验证码错误！'
            return render(request,'checkEmailyanz.html',locals())
    return render(request,'checkEmailyanz.html',locals()) 

def checkcodgetin(request):
    #mstream = StringIO()
    mstream = io.BytesIO()
    #print("1231")
    validate_code = Checkcode.create_validate_code()#引用自己写的Checkcode脚本(python函数)
    img = validate_code[0]
    #print(type(img))
    #print(type(mstream))
    img.save(mstream, "GIF")
    #print("img")
    #将验证码保存到session
    request.session["checkcodforgetpassw"] = validate_code[1]
    v_code = validate_code[1]
    #print(v_code)
    #return render(request, 'WantBuy.html', locals())
    return HttpResponse(mstream.getvalue())
def staffdeletein(request):
    print("删除员工")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(request.GET)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')  
    if request.POST:
        v_staffnumber =request.POST['staffnumber']
        print(v_staffnumber)
        #staffinfo.objects.filter(staffnumber=v_staffnumber).update(isfail = -1)
        searchstaffinfolists=staffinfo.objects.filter(staffnumber=v_staffnumber)  
        #根据传进来的编号以及checklist来更新员工表isfail为-1.
        #返回员工信息。
    return render(request, 'staffdelete.html', locals())
def searchstaffdeletein(request):
    print("搜索删除员工") 
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(request.GET)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')  
    if request.GET:
        print("搜索")
        print("---------searchsstaffdeletein--------")
        searchsstaffdelete =request.GET['q']
        print(searchsstaffdelete)
        searchstaffinfolists=staffinfo.objects.filter(staffname__icontains=searchsstaffdelete)  
        print(searchstaffinfolists)
        #搜索员工表，返回员工信息，编号、姓名、部门、单位、身份证、手机号、isfail:大于0是激活，小于0是已注销。
        print("---------searchsstaffdeletein--------")
    return render(request, 'staffdelete.html', locals())
 
def staffinsertin(request):
    print("新增员工信息")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0') 
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')
    deptmentlists=deptment.objects.filter(isfail='0')  
    unitlists = list(staffinfo.objects.values_list('staffunit').annotate(Count('id'))) 
    #print(unitlists.query) 
    if request.POST:
        v_name =request.POST['staffname']
        v_sex =request.POST['sexcheck']
        v_dept =request.POST['deptcheck']
        v_unit =request.POST['unitcheck']
        v_addr =request.POST['addr']  
        v_idcard = request.POST['idcard']
        v_email = request.POST['Email']
        v_phone = request.POST['phone']
        v_oa = request.POST['oaccount'] 
        staffinfolists=staffinfo.objects.filter(staffidcard=v_idcard)
        #staffinfolists=staffinfo.objects.filter(staffname=v_name)
        if staffinfolists:
            #员工表里面有人
            return render(request, 'errstaffinsert.html', locals())
        print("---------staffinfo--------")
        print(v_name)
        print(v_dept)
        print(v_unit)
        print(v_sex)
        print(v_addr)
        print(v_idcard)
        print(v_email)
        print(v_phone)
        print(v_oa)
        print("---------staffinfo--------") 
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
        #staffnumber
        #staffinfolists.objects.create(staffname=v_name,staffdept = v_dept ,staffunit = v_dept, staffsex = v_sex,staffphone = v_phone,staffemail = v_email,staffoaccount = v_oa,staffidcard =v_idcard, staffworkplace = v_addr,staffpw='123456',staffclass=1,createtime=time,updatetime=time,isfail="0")
    
        return render(request, 'successfulstaffinsert.html', locals())
     
    return render(request, 'staffinsert.html', locals())
def sportsupdatein(request):
    print("更新活动")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(request.GET)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')  
    if request.POST: 
        print("---------锁定更新的活动--------")
        v_sportnumber =request.POST['sportnumber']
        print(v_sportnumber)
        sportupdateinfolists=sportlist.objects.filter(sportnumber=v_sportnumber)
        print("---------锁定更新的活动--------")
    return render(request, 'sportsupdateinfo.html', locals())

def sportsupdateinfoin(request):
    print("更新活动信息")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(request.GET)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login')  
    if request.POST: 
        print("---------更新活动信息写入数据库--------") 
        i_sportnumber =request.POST['sportnumber'] 
        i_sportname =request.POST['Sportname']
        i_sportcontent =request.POST['Sportcontent'] 

        sportstartdate =request.POST['sportstarttime']
        sportenddate =request.POST['sportendtime']
        sporttype =request.POST['sporttype']
        print(i_sportnumber)
        print(i_sportname)
        #sportlist.objects.filter(sportnumber=v_sportnumber)
        '''
        sportlist.objects.filter(sportnumber=v_sportnumber).update(sportname = i_sportname) 
        sportlist.objects.filter(sportnumber=v_sportnumber).update(sportcontent = i_sportcontent) 
        sportlist.objects.filter(sportnumber=v_sportnumber).update(sportstartdate = sportstartdate) 
        sportlist.objects.filter(sportnumber=v_sportnumber).update(sportenddate = sportenddate) 
        sportlist.objects.filter(sportnumber=v_sportnumber).update(sporttype = sporttype)  
        '''

 
        #搜索活动表，返回活动信息，编号、名字、内容、状态。
        #跳转到另一个界面修改，提交，只能修改内容，名字和状态。
        print("---------更新活动信息写入数据库--------")
    return render(request, 'successfulsportupdate.html', locals()) 
def sportsearchupdatein(request):
    print("查看修改活动")
    staff_name = request.session.get('staff_name','游客')
    staff_id = request.session.get('staff_id','0')
    staff_class = request.session.get('staff_class','0')
    print(request.GET)
    if staff_id == '0':
        #return render(request, 'login.html', locals())
        return HttpResponseRedirect('/login')
    if staff_class <'3':
        del request.session['staff_name']  #删除session
        del request.session['staff_id']  #删除session
        del request.session['staff_class']  #删除session
        return HttpResponseRedirect('/login') 
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S") 
    if request.GET:
        print("搜索")
        print("---------searchsportupdate--------")
        searchsportupdate =request.GET['q']
        print(searchsportupdate) 
        searchsportlists=sportlist.objects.filter(sportname__icontains=searchsportupdate) 
        print("---------searchsportupdate--------") 
        print(searchsportlists)
     
    
    return render(request, 'sportsupdate.html', locals())
 