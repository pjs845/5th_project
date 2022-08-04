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

# DB 불러오기
url = "mongodb://192.168.0.66:27017"
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
from .models import Member #회원정보   
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