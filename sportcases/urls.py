"""sportcases URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from home import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'^index/$',views.index,name='index'),
    url(r'^insertsport$',views.insertsportin),
    url(r'^insearchsports$',views.insearchsportsin),
    url(r'^increatesport/$',views.createsportin),
    url(r'^insendEmailsports/$',views.sendEmailsportsin),
    url(r'^inaddrequestattr/$',views.addrequestattrin),
    url(r'^insearchsport/(?P<id>\d+)/$',views.searchsportin), 
    url(r'^injoinsport/(?P<id>\d+)/$',views.joinsportin), 
    url(r'^checkdepartment$',views.checkdepartmentin, name='add'), 
    url(r'^inexpsportinfo/$',views.expsportinfoin, name='add'), 
    url(r'^indownload_file/(?P<deptnumber>.+)_(?P<sports>\d+)/$',views.download_filein),
    url(r'^staffinfo/$',views.staffinfoin,name='staffinfoin'),
    url(r'^staffinfoadmin/$',views.staffinfoadmin,name='staffinfoadmin'),
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^insportconfirm/(?P<sid>\d+)/$',views.sportconfirmin), 
    url(r'^absentreason/(?P<sid>\d+)/$',views.absentreasonin,name='logout'),   
    url(r'^inconfirmtrue/(?P<sid>\d+)/$',views.confirmtruein,name='logout'),   
    url(r'^inupdatesportstaffinfo/(?P<sid>\d+)/$',views.updatesportstaffinfoin,name='logout'),
    url(r'^instaffsearchsports/$',views.staffsearchsportsin),
    url(r'^inforgetpassw/$',views.forgetpasswin),
    url(r'^inforgetpasswyanz/$',views.forgetpasswyanzin), 
    url(r'^inforgetpasswuppw/$',views.forgetpasswuppwin), 
    url(r'^incheckEmail/$',views.checkEmailin), 
    url(r'^incheckEmailyanz/$',views.checkEmailyanzin), 
    url(r'^checkcodget/$',views.checkcodgetin),
    url(r'^instaffdelete/$',views.staffdeletein),
    url(r'^insearchstaffdelete/$',views.searchstaffdeletein),
    url(r'^instaffinsert/$',views.staffinsertin),
    url(r'^insportsupdate/$',views.sportsupdatein),
    url(r'^insportsearchupdate/$',views.sportsearchupdatein),
    url(r'^insportsupdateinfo/$',views.sportsupdateinfoin),
    url(r'^news/$',views.newsin),
    url(r'^coupons/$',views.couponsin),
    url(r'^vedios/$',views.vediosin),
    url(r'^games/$',views.gamesin),
    url(r'^games/(?P<changeid>\d+)/$',views.gameschangein),
    url(r'^games/(?P<changeid>\d+)/info/$',views.gameschangeinfoin),
    url(r'^gamesinfostart/(?P<changeid>\d+)/$',views.gamesinfostartin),
    url(r'^gameschangeend/(?P<changeid>\d+)/$',views.gameschangeendin),

    
    
    
    

     

]
 