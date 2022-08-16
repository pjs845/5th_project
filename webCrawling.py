from pymongo import mongo_client
from bs4 import BeautifulSoup
import requests
import pandas as pd
from bs4 import BeautifulSoup


id = 1
#몽고DB
host = "192.168.0.66"
port = 27017
client = mongo_client.MongoClient(host, port)
db = client["CampMain"]
col = db["Camp"]  
col.drop()
#페이지 크롤링
url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=last_updusr_pnttm&pageIndex=1"
response = requests.get(url)
source = response.text
# print(source)

soup = BeautifulSoup(source, "html.parser")
# 1. 필요한 정보 가져오는 테스트 
# # camp_info = soup.find("div", id="cont_inner")
# print(camp_info)


# 2. 마지막 페이지 가져오기 
# 2-1. 마지막 페이지를 가져오려다 보니 id, class가 없어 find() 함수가 아닌 select_one 함수를 이용해 함
li = soup.select_one("#cont_inner > div > div.paging > ul > li:nth-child(14) > a")
x = li["href"]
y = x.split("=")
print(y)
last_page = y[-1]
print(last_page)

# 각 페이지 읽어오기 ( 마지막 311페이지까지 )
import pandas as pd
df = pd.DataFrame()
base_url = "https://www.gocamping.or.kr/bsite/camp/info/list.do?pageUnit=10&searchKrwd=&listOrdrTrget=last_updusr_pnttm"
for page in range(1, int(last_page)+1): # 311페이지가 마지막이라 +1
#for page in range(1, 2): #너무 많아서 2페이지만 테스트 하기용
    url = "{}&pageIndex={}".format(base_url, page) # page 부분이 1~ 311까지 반복
    response = requests.get(url, headers={"User-agent":"Mozilla/5.0"})
    source = response.text
    soup = BeautifulSoup(source, "html.parser")
    camps_info = soup.find("div", class_="camp_search_list") # 한 페이지에 캠핑정보 전체 긁어오기
    camp_info = soup.find("div", class_ ="camp_cont") # 한 문단의 정보씩 //근데 첫문단 밖에 안됨
    for x in range(1,11):
        comp_bar1 = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > p > span.item_t01")
        comp_bar2 = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > p > span.item_t02")
        comp_bar3 = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > p > span.item_t03")
        comp_bar4 = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > p > span.item_t04")
        comp_loc = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > h2 > a")
        comp_exp = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > span.camp_txt > a")
        comp_loc2 = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > ul > li.addr")
        comp_num = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > ul > li.call_num")
        comp_Facilities = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > div > div")
        comp_image = soup.select_one("#cont_inner > div > div.camp_search_list > ul > li:nth-child("+str(x)+") > div > a > div > img")
        img = """<img src="https://www.gocamping.or.kr"""+comp_image['src']+"""" height="180" width="280">"""
        
        if comp_num == None:  
            dict = {"_id":id,"사업체":comp_bar1.text,"리뷰수":comp_bar2.text,"조회수":comp_bar3.text,"추천수":comp_bar4.text,"캠핑장이름":comp_loc.text,"캠핑장설명":comp_exp.text,"지역이름":comp_loc2.text,"전화번호":"None","캠핑장정보":"None", "이미지":img}
            col.insert_one(dict)
            
        else:
            #print(comp_num.text)
            dict = {"_id":id,"사업체":comp_bar1.text,"리뷰수":comp_bar2.text,"조회수":comp_bar3.text,"추천수":comp_bar4.text,"캠핑장이름":comp_loc.text,"캠핑장설명":comp_exp.text,"지역이름":comp_loc2.text,"전화번호":comp_num.text,"캠핑장정보":"None", "이미지":img}
            col.insert_one(dict)
            
            
        if comp_Facilities == None:
            pass
        else:
            where = {"_id":id} 
            new = {"$set": {"캠핑장정보":comp_Facilities.text}}
            col.update_one(where, new)
            
        id+=1