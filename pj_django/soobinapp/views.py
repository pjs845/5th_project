from asyncio.windows_events import NULL
from tabnanny import check
from typing import List
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from soobinapp.models import Address, Board, Member
from django.db.models import Q

# def index(request):
#     return HttpResponse("<center><h2>안녕 장고</h2></center>")

def index(request):
    template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    return HttpResponse(template.render({}, request)) # 반드시 request를 넘겨줘야 함

def list(request):
    template = loader.get_template('list.html')
    # addresses = Address.objects.all().values() # 전체
    # addresses = Address.objects.filter(name='또치', addr='서울시').values()
    # addresses = Address.objects.filter(name='또치').values() | Address.objects.filter(addr='서울시').values() # or 
    # addresses = Address.objects.filter(Q(name='또치') | Q(addr='서울시')).values()
    # addresses = Address.objects.filter(name__startswith='호').values()
    # addresses = Address.objects.filter(rdate__hour='22').values()
    # addresses = Address.objects.all().order_by('name').values() # order by asc
    # addresses = Address.objects.all().order_by('-name').values() # order by desc
    addresses = Address.objects.all().order_by('-name', '-id', '-addr').values() # order by desc
    context = {
        'addresses': addresses,
    }
    return HttpResponse(template.render(context, request))

def write(request):
    template = loader.get_template('write.html')
    return HttpResponse(template.render({}, request))

from django.urls import reverse
from django.utils import timezone
def write_ok(request):
    x = request.POST['name']
    y = request.POST['addr']
    time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    address = Address(name=x, addr=y, rdate=time)
    address.save()
    return HttpResponseRedirect(reverse('list'))

def delete(request, id):
    address = Address.objects.get(id=id)
    address.delete()
    return HttpResponseRedirect(reverse('list'))

def update(request, id):
    template = loader.get_template('update.html')
    address = Address.objects.get(id=id)
    context = {
        'address':address,
    }
    return HttpResponse(template.render(context, request))

def update_ok(request, id):
    x = request.POST['name']
    y = request.POST['addr']
    address = Address.objects.get(id=id)
    address.name = x
    address.addr = y
    address.rdate = timezone.now()
    address.save()
    return HttpResponseRedirect(reverse('list'))

###############################################
from django.core.paginator import Paginator
def page_list(request):
    template = loader.get_template('b_list.html')
    print(request.GET.get('page'))
    page = request.GET.get('page',1)
    board_list = Board.objects.all().order_by('-id').values()
    paginator = Paginator(board_list, 5) # 페이지 표시 수
    page_obj = paginator.get_page(page)
        
    context = {
        'page_obj':page_obj,
    }
    return HttpResponse(template.render(context, request))
###############################################

# def b_list(request):
#     template = loader.get_template('b_list.html')
#     boards = Board.objects.all().values()
#     context = {
#         'boards':boards,
#     }
#     return HttpResponse(template.render(context, request))

################################################

def b_write(request):
    template = loader.get_template('b_write.html')
    return HttpResponse(template.render({}, request))

def b_write_ho(request):
    na = request.POST['b_name']
    e = request.POST['b_email']
    t = request.POST['b_title']
    c = request.POST['b_content']
    current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    board = Board(b_name=na, b_email=e, b_title=t, b_content=c, b_rdate=current_time)
    board.save()
    return HttpResponseRedirect(reverse('page_list'))

def b_revise(request, id):
    template = loader.get_template('bb_content.html')
    board = Board.objects.get(id=id)
    context = {
        'board':board,
    }
    return HttpResponse(template.render(context, request))

def b_update(request, id):
    template = loader.get_template('b_update.html')
    board = Board.objects.get(id=id)
    context = {
        'board':board,
    }
    return HttpResponse(template.render(context, request))

def b_update_ho(request, id):
    na = request.POST['b_name']
    e = request.POST['b_email']
    t = request.POST['b_title']
    c = request.POST['b_content']
    board = Board.objects.get(id=id)
    board.b_name = na
    board.b_email = e
    board.b_title = t
    board.b_content = c
    current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    board.b_rdate = current_time
    board.save()
    return HttpResponseRedirect(reverse('page_list'))

def b_delete(request, id):
    board = Board.objects.get(id=id)
    board.delete()
    return HttpResponseRedirect(reverse('page_list'))

################ MEMBER ###################
def login(request):
    # template = loader.get_template('login.html') # 방법 1 
    # return HttpResponse(template.render({},request)) # 방법 1
    return render(request, 'login.html') # 방법 2 

def login_ok(request):
    # mail = request.POST['m_email']
    # pwd = request.POST['m_pwd']
    mail = request.POST.get('m_email', None) # 값 가져오기
    pwd = request.POST.get('m_pwd', None) # 값 가져오기
    print("email:",mail, "pass:",pwd) # 로그인 페이지에서 입력 값 가져오는지 확인
    try:
        member = Member.objects.get(m_email=mail)
    except Member.DoesNotExist:
        member = None
    # print("멤버:",member) # 해당하는 멤버의 행?이 검색됨
    
    result_num = 0
    if member != None:
        print("회원 이메일 존재함")
        if member.m_pwd == pwd:
            print("비밀번호도 일치함")
            result_num = 1
            print("member.m_email:", member.m_email) # 방법1
            request.session['login_check'] = member.m_email # 방법1
            
            # session_id = request.session.session_key # 방법2
            # print ("session_id:", session_id) # 방법2
            # request.session['login_check'] = session_id 방법2
        else:
            print("비밀번호는 틀림")
            result_num = 2
    else:
        print("회원 이메일 존재하지 않음")
        result_num = 3
    
    template = loader.get_template("login_ok.html")
    context = {
        'result_num':result_num,
    }
    return HttpResponse(template.render(context, request))


def logout(request):
    if request.session.get('login_check'):
        del request.session['login_check']
        #request.session.clear() # 서버측의 해당 user의 session방을 초기화
		#request.session.flush() # 서버측의 해당 user의 session방을 삭제
    return redirect("../")


def test1(request):
    addresses = Address.objects.all().values()
    template = loader.get_template("template1.html")
    context = {
        'yourname':'길동',
        'addresses':addresses,
    }
    return HttpResponse(template.render(context, request))

def test2(request):
    template = loader.get_template("template2.html")
    context = {
        'x': 2,
        'y': 'tiger',
        'fruits': ['apple', 'orange'],
        'z': 2,
    }
    return HttpResponse(template.render(context, request))


def test3(request):
    addresses = Address.objects.all().values()
    
    template = loader.get_template("template3.html")
    context = {
        'fruits': ['apple', 'orange', 'melon'],
        'cars': [{'brand':'현대', 'model':'소나타', 'year':'2022'}, {'brand':'테슬라', 'model':'모델X', 'year':'2020'}],
        'addresses':addresses,
    }
    return HttpResponse(template.render(context, request))

def test4(request):
    template = loader.get_template("template4.html")
    context = {
        'name':'홍길동',
    }
    return HttpResponse(template.render(context, request))

def test5(request):
    addresses = Address.objects.all().values()
    template = loader.get_template("template5.html")
    context = {
        'addresses':addresses,
    }
    return HttpResponse(template.render(context, request))

def test6(request):
    addresses = Address.objects.all().values()
    template = loader.get_template("template6.html")
    context = {
        'addresses':addresses,
    }
    return HttpResponse(template.render(context, request))

def test7(request):
    template = loader.get_template("template7.html")
    context = {
    }
    return HttpResponse(template.render(context, request))
# from pymongo import mongo_client
# url = "mongodb://192.168.0.66:27017"
# mgClient = mongo_client.MongoClient(url)
# db = mgClient["CampMain"]
# col = db["CampInfo"]
# docs = col.find()
# a = []
# for x in docs:
#     # a.append(x.get('_id'))
#     a.append(x)
# print(a)
def test8(request):
    template = loader.get_template("template8.html")
    context = {
        # 'a':a,
    }
    return HttpResponse(template.render(context, request))



#추가
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from pymongo import mongo_client
from bs4 import BeautifulSoup



url = "mongodb://192.168.0.66:27017"
mgClient = mongo_client.MongoClient(url)
db = mgClient["CampMain"]
col = db["CampInfo"]
docs = col.find()
a = []
camps = []
i = 0
for x in docs:
    #a.append(x.get('_id'))
    a.append(x)
    soup = BeautifulSoup(x['이미지'])
    imgs = soup.find_all("img")
    for y in imgs:
        camp = {"name":x["캠핑장이름"],"addr": x["지역이름"], "img":y["src"]}
        camps.append(camp)
    i += 1
    if i == 6:
        break


def test9(request):
    template = loader.get_template("pj_main.html")
    context = {
        'infolen':len(a),
        'camps':camps
    }
    return HttpResponse(template.render(context, request))


