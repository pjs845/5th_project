from types import MemberDescriptorType
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone

# 추가
from pymongo import mongo_client
from bs4 import BeautifulSoup
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Notice
from .models import Member #회원정보 

# DB 불러오기
url = "mongodb://localhost:27017"
mgClient = mongo_client.MongoClient(url)
db = mgClient["CampMain"]
col = db["CampInfo"]
docs = col.find()
a = []
camps = []
for x in docs:
    #a.append(x.get('_id'))
    a.append(x)
    soup = BeautifulSoup(x['이미지'])
    imgs = soup.find_all("img")
    for y in imgs:
        name = x["캠핑장이름"][x["캠핑장이름"].find("]")+1:]
        camp = {"name":name,"addr": x["지역이름"], "img":y["src"]}
        camps.append(camp)
  
########## 메인 페이지  ##########
def main_page(request):
    template = loader.get_template("pj_main.html")
    context = {
        'camps':camps,
    }
    return HttpResponse(template.render(context, request))

########## 메인 페이지 -( 페이징 )- ##########

def paging(request):
    template = loader.get_template("paging.html")
    context = {
        'camps': camps,
    }
    return HttpResponse(template.render(context, request))

########## login 페이지 ##########
def login(request):
   return render(request,'login.html')

########## login_ok(조건) ##########
def login_ok(request):
    email = request.POST.get('email',None) 
    pwd = request.POST.get('password1', None) 
    #print("email", email, "pwd", pwd)
    try:
      member = Member.objects.get(email=email)   
    except Member.DoesNotExist:
      member = None 
    result = 0
    if member != None:
        if member.password1 == pwd:
            result = 2
            request.session['login_ok_user'] = member.email 
        else:
            result = 1
    else:
        result = 0   
    temlate = loader.get_template("login_ok.html")
    context = {
        'result': result, 
    }
    return HttpResponse(temlate.render(context, request))

########## logout ##########
def logout(request):
    if request.session.get('login_ok_user'):
        del request.session['login_ok_user']
        #request.session.clear() # 서버측의 해당 user의 session방을 초기화
        request.session.flush() # 서버측의 해당 user의 session방을 삭제
    return redirect("../")

########## signup 페이지 ##########
def signup(request):
    template = loader.get_template("signup.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

########## signup_ok (조건) ##########
def signup_ok(request):
   if request.method == "POST":
      if request.POST['password1'] == request.POST['password2'] :
         a = request.POST['name']
         b = request.POST['email']
         c = request.POST['phone']
         d = request.POST['password1']
         nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') 
         member = Member(name = a, email = b, phone = c, password1 = d, rdate=nowDatetime, udate=nowDatetime)
         member.save()
         return HttpResponseRedirect(reverse('main'))

########## 서브 페이지 ##########
def board_page(request): #게시판으로 가는 페이지 연동
    template = loader.get_template("board.html")
    context = {
    }
    return HttpResponse(template.render(context, request))

########## 광고 페이지 ##########
def ad_page(request): #서브로 가는 페이지 연동
    template = loader.get_template("ad.html")
    context = {
        
    }
    return HttpResponse(template.render(context, request))

########## 공지사항 페이지 ###########
def notice(request): #서브로 가는 페이지 연동
    template = loader.get_template("notice.html")
    notices = Notice.objects.all().order_by('-id').values()
    context = {
        "notices":notices
    }
    return HttpResponse(template.render(context, request))

########## 공지사항 내용 페이지 #############
def content(request, id):
    template = loader.get_template('content.html')
    contents = Notice.objects.get(id=id)
    contents.count += 1
    contents.save()
    context = {
        'content': contents,
    }
    return HttpResponse(template.render(context, request))

########## 공지사항 검색 ##################
from django.db.models import Q

def search(request):
    notice = Notice.objects.all().order_by('-id')
    q = request.POST.get('q', "") 
    if q:
        notice = notice.filter(Q (subject__contains=q) | Q (content__contains=q))
        print("notice: ")
        return render(request, 'notice.html', {'notices' : notice, 'q' : q})
    
    else:
        return render(request, 'notice.html')
    
    
########## search 페이지 검색 기능 ##########
def search_page(request):
    return render(request, 'pj_main.html')   
    
########## search 페이지 ##########
search_camp = []
from django.core.paginator import Paginator
def search_subpage(request):
    # template = loader.get_template('searching.html')
    ca_na = request.POST.get('camp_name', None)
    print("form값 체크:",ca_na)
    where = {"캠핑장이름":{"$regex":ca_na}}
    f = col.find(where)
    for x in f:
        # print(x)
        soup2 = BeautifulSoup(x['이미지'])
        image = soup2.find_all("img")
        for win in image:
            na = x["캠핑장이름"]
            searching = {"na":na,"addr": x["지역이름"], "img":win["src"]}
            search_camp.append(searching)
    template = loader.get_template('findpage.html')
    page = request.GET.get('page', 1)
    paginator = Paginator(search_camp, 9999) # 한 페이지안에 표시 수
    page_obj = paginator.get_page(page)       
    context = {
        'page_obj':page_obj,
        'ca_na':ca_na,
    }
    search_camp.clear()
    return HttpResponse(template.render(context, request))
