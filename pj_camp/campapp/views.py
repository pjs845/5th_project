from pyexpat.errors import messages
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
from .models import Notice, Board_Comment
from .models import Member #회원정보 

# DB 불러오기
url = "mongodb://192.168.0.66:27017"
mgClient = mongo_client.MongoClient(url)
db = mgClient["CampMain"]
col = db["Camp"]
docs = col.find()
camps = []
for x in docs:
    id = x.get('_id')
    soup = BeautifulSoup(x['이미지'])
    imgs = soup.find_all("img")
    
    for y in imgs:
        name = x["캠핑장이름"][x["캠핑장이름"].find("]")+1:]
        camp = {"id":id,"name":name,"addr": x["지역이름"], "img":y["src"]}
        camps.append(camp)
  
###### 서프페이지 #######
def sub_page(request,id):
    db_sub = mgClient["CampPage"]
    col_sub = db_sub["Info"]
    template = loader.get_template("template1.html")
    sub = col.find({"_id":id})
    for x in sub:
        addr = x.get("지역이름").strip()
        name = x["캠핑장이름"][x["캠핑장이름"].find("]")+1:]
        print(name)
        k = col_sub.find({"주소":addr})
        a11 = x.get("이미지")
        soup = BeautifulSoup(a11)
        imgs = soup.find_all("img")
        
        for y in imgs:
            for x1 in k:
                try:
                    facil1 = x1['주변이용가능시설'].split(',')  
                except:
                    facil1 = None
                try:
                    facil2 = x1['카라반내부시설'].split('\n')
                except:
                    facil2 = None
                try:
                    facil3 = x1['글램핑내부시설'].split('\n')
                except:
                    facil3 = None
                try:
                    animal = x1['기타정보'].split('반려')
                    print(animal) 
                    if ' 불가능' in animal[1]:
                        animal = '반려동물 동반 불가능'
                    elif '가능' in animal[1]:
                        animal = '반려동물 동반 가능'
                except:
                    animal = None
                if '소화기' in x1['안전시설현황']:
                    fire = '소화기'
                else:
                    fire = None
                if '화재감지기' in x1['안전시설현황']:
                    feel = '화재경보기'
                else:
                    feel = None
                print(x1['안전시설현황'])
                context = {
                    'x1':[x1],
                    'img':y["src"],
                    'facil':{'facil1':facil1,'facil2':facil2,'facil3':facil3,'소화기':fire,'화재경보기':feel},
                    'animal':animal,
                    'camps':camps,
                    'addr':[{'addr1':addr,'name':name}],
                }

    return HttpResponse(template.render(context, request))

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
        request.session.clear() 
        request.session.flush() # 서버측의 해당 user의 session방을 삭제
    return redirect("../")


########## signup 페이지 ##########
def signup(request):
    return render(request,'signup.html')

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
         return HttpResponseRedirect(reverse('login'))

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
    notice_fixed = Notice.objects.filter(top_fixed=True).order_by('-rdate')
    context = {
        "notices":notices,
        "notice_fixed": notice_fixed
    }
    return HttpResponse(template.render(context, request))

########## 공지사항 내용 페이지 #############
def content(request, id):
    template = loader.get_template('content.html')
    contents = Notice.objects.get(id=id)
    contents.count += 1
    contents.save()
    filename = str(contents.upload_files)
    filename = filename.split('/')[-1]

    context = {
        'content': contents,
        'filename':filename,
    }
    return HttpResponse(template.render(context, request))

########## 공지사항 검색 ##################
from django.db.models import Q

def search(request):
    notice = Notice.objects.all().order_by('-id')
    q = request.POST.get('q', "") 
    if q:
        notice = notice.filter(Q (subject__contains=q) | Q (content__contains=q))
        return render(request, 'notice.html', {'notices' : notice, 'q' : q})
    
    else:
        return render(request, 'notice.html')
    

############# 공지사항 파일 다운로드 ##################
import urllib
import os
from django.http import HttpResponse, Http404
import mimetypes
from django.shortcuts import get_object_or_404

def notice_download_view(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    url = notice.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)
    
    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            filename = str(notice.upload_files)
            filename = filename.split('/')[-1]
            quote_file_url = urllib.parse.quote(filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404
    
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
            searching = {"id":x['_id'],"na":x["캠핑장이름"],"addr": x["지역이름"], "img":win["src"]}
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

########## 글쓰기 페이지 ##########
from .models import Board #게시판

def write_page(request):
    return render(request, 'write.html')   

def board(request):
    template = loader.get_template('board.html')
    board = Board.objects.all().order_by('-id')
    
    context = {
		'boards': board, 
	}
    return HttpResponse(template.render(context, request))

def write_page(request):
         template = loader.get_template('write.html')
         try:
            member = Member.objects.get(email=request.session['login_ok_user'])
         except KeyError:
            member = None 
         context = {
            'member':member    
         }
         return HttpResponse(template.render(context, request))	

def write_ok(request):
    try:
            member = Member.objects.get(email=request.session['login_ok_user'])
    except KeyError:
            member = None 
    y = request.POST['title']
    z = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boards =  Board(writer=member, title=y, content=z, rdate=nowDatetime)
    boards.save()
    return HttpResponseRedirect(reverse('board'))

from datetime import date, datetime, timedelta

def detail(request, id):
    try:
        member = Member.objects.get(email=request.session['login_ok_user'])
    except KeyError:
        member = None
    login_session = request.session.get('login_ok_user', '')
    
    board = Board.objects.get(id=id)
    comment = Board_Comment.objects.all()
    comment = comment.filter(Q (post=board))
    if board.writer.email == login_session:
        board_writer = True
    else:
        board_writer = False
    context = {
        'boards': board,  
        'members': member,
        'comments': comment,
        'login_session': login_session,
        'board_writer': board_writer,
    }  
    response = render(request, 'detail.html', context)
    
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    
    cookie_value = request.COOKIES.get('counts', '_')
    if f'_{id}_' not in cookie_value:
        cookie_value += f'{id}_'
        response.set_cookie('counts', value=cookie_value, max_age=max_age, httponly=True)
        board.hits += 1
        board.save()
    return response

def update(request, id):
    template = loader.get_template('update.html')
    boards = Board.objects.get(id=id) 
    context = {
        'boards': boards,  
    }  
    return HttpResponse(template.render(context, request))

def update_ok(request, id):
    y = request.POST['title']
    z = request.POST['content']
    board = Board.objects.get(id=id)
    board.title = y
    board.content = z
    board.save()
    return HttpResponseRedirect(reverse('board'))

def delete(request, id):
    board = Board.objects.get(id=id)
    print(board)
    comment = Board_Comment.objects.all()
    comment = comment.filter(Q (post__id__contains=id))
    board.delete()
    comment.delete()
    return HttpResponseRedirect(reverse('board'))

########## 게시판 검색 ##################
from django.db.models import Q

def board_search(request):
    board = Board.objects.all().order_by('-id')
    comment = Board_Comment.objects.all()
    f = request.POST.get('cate1', "")
    q = request.POST.get('q', "") 
    print("f:", f)
    print("q:", q)
    if q:
        if f == "all":
            board = board.filter(Q (title__contains=q) | Q (content__contains=q))    
        elif f == "title":
            board = board.filter(Q (title__contains=q))    
        elif f == "content":
            board = board.filter(Q (content__contains=q))    
        elif f == "writer":
            board = board.filter(Q (writer__name__contains=q))  
            print(board)  
        elif f == "comment":
            comment = comment.filter(Q (content__contains=q)).values_list('post')
            print(comment)
            board = board.filter(Q (id__in=comment))
            print(board)
        return render(request, 'board.html', {'boards' : board, 'q' : q})
    
    else:
        return render(request, 'board.html')



########## 댓글 삭제 ################
def delete_comment(request, num, id):
    comment = Board_Comment.objects.get(id=id)
    comment.delete()
    return redirect('../../../'+str(num))


from django.urls import reverse_lazy
######### 댓글 달기 ##############
def comment_write(request, phone, id):
    comment = get_object_or_404(Board, pk=id)
    print("comment:", comment)
    contents = request.POST.get('content')
    member = Member.objects.get(phone=phone)
    print("member:", member)
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not content:
        messages.info(request, '댓글을 입력해주세요')
        return HttpResponseRedirect(reverse('detail', args=[id]))
    Board_Comment.objects.create(post=comment, writer=member, content=contents, rdate=nowDatetime)
    return HttpResponseRedirect(reverse('detail', args=[id]))

########## 비밀번호 찿기 ##########
def forgot_password(request):
   temlate = loader.get_template('forgot_password.html')
   return HttpResponse(temlate.render({}, request))

def forgot_password_ok(request):
   if request.method == "POST":
      name = request.POST['name']
      email = request.POST['email']
      member =  Member.objects.get(name = name, email = email)
      print(member.password1)
      #esle->try,cacth로 dosenotexist 
      return HttpResponseRedirect(reverse('main'))


########### 지도 페이지 ################
def map(request):
    template = loader.get_template('map.html')
    context = {
        'camps':camps
    }
    return HttpResponse(template.render(context, request))	


########## 마이페이지 ##########    
def mypage(request):
    temlate = loader.get_template('mypage.html')
    member = Member.objects.get(email = request.session['login_ok_user'])
    context = {
    'member' : member 
    }   
    return HttpResponse(temlate.render(context, request))    
########## 회원정보수정 ##########   
def updateinfo(request):
    template = loader.get_template("updateinfo.html")
    member = Member.objects.get(email = request.session['login_ok_user'])
    context = {
      'member': member  
    }
    return HttpResponse(template.render(context, request))
def updateinfo_ok(request):
    email = request.POST['email']
    phone = request.POST['phone']
    member = Member.objects.get(email = request.session['login_ok_user'])   
    member.email = email
    member.phone = phone
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    member.rdate = nowDatetime
    member.save()
    request.session['login_ok_user'] = member.email
    return HttpResponseRedirect(reverse('mypage'))   
########## 기존비밀번호확인 ##########
def checkpassword (request) : 
    temlate = loader.get_template("checkpassword.html")
    return HttpResponse(temlate.render({}, request))

def checkpassword_ok(request):
   if request.method == "POST":
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    member = Member.objects.get(email = request.session['login_ok_user'])
    if password1 == password2 :
        return HttpResponseRedirect(reverse('resetpassword'))
########## 비밀번호 변경 ##########
def resetpassword (request):
    temlate = loader.get_template("resetpassword.html")
    return HttpResponse(temlate.render({}, request))
def resetpassword_ok(request):
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    if password1 == password2 : 
        member = Member.objects.get(email = request.session['login_ok_user'])   
        member.password1 = password1
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        member.rdate = nowDatetime
        member.save()
        request.session['login_ok_user'] = member.email
        return HttpResponseRedirect(reverse('main'))   
########## 탈퇴(비밀번호확인) ##########
def deleteAcount(request) : 
    temlate = loader.get_template("deleteAcount.html")
    return HttpResponse(temlate.render({}, request))
def deleteAcount_ok(request):
   if request.method == "POST":
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    member = Member.objects.get(email = request.session['login_ok_user'])
    if password1 == password2 :
        if member.password1 == password1:
            member.delete()
            del request.session['login_ok_user']
            request.session.flush() # 서버측의 해당 user의 session방을 삭제
        return HttpResponseRedirect(reverse('main'))