from pymongo import mongo_client
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

host = "localhost"
port = 27017
client = mongo_client.MongoClient(host, port)
db = client["Camp"]
col = db["Info"]  
# col.drop()

a = list(range(1,8220))
for x in range(99997,100600):
    a.append(x)
# 상세 페이지 패널1. 크롤링
for x in a:
    if x == 2474:
        continue
    
    base_url = "https://www.gocamping.or.kr/bsite/camp/info/read.do?c_no="+str(x)+"&viewType=read01&listOrdrTrget=frst_register_pnttm"
    response = requests.get(base_url)
    source = response.text
    soup = BeautifulSoup(source, "lxml")

    # 캠프 이름
    camp_name = soup.find("p", class_="camp_name")
    # Panel1 - option 1
    detail1 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(1)")
    # Panel1 - option 2
    detail2 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(2)")
    # Panel1 - option 3
    detail3 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(3)")
    # Panel1 - option 4
    detail4 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(4)")
    # Panel1 - option 5
    detail5 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(5)")
    # Panel1 - option 6
    detail6 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(6)")
    # Panel1 - option 7
    detail7 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(7)")
    # Panel1 - option 8
    detail8 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(8)")
    # Panel1 - option 9
    detail9 = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table > tbody > tr:nth-child(9)")
    # Panel1 Main ( 페이지 있는지 판단 )
    info = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table") # 1번째 문단
    
    if info == None:
        print("페이지 없음", x)
        pass
    else:
        if detail3 == None:
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))   
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1])}
            col.insert_one(dict)
            
        elif detail4 == None:
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            d3 = detail3.text.strip().split("\n",1)
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))
            print(d3[0], re.sub(r"\s", "", d3[1]))
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1]),re.sub(r"\s", "", d3[0]):re.sub(r"\s", "", d3[1])}
            col.insert_one(dict)
         
        elif detail5 == None:
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            d3 = detail3.text.strip().split("\n",1)
            d4 = detail4.text.strip().split("\n",1)
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))
            print(d3[0], re.sub(r"\s", "", d3[1]))
            print(d4[0], re.sub(r"\s", "", d4[1]))
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1]),re.sub(r"\s", "", d3[0]):re.sub(r"\s", "", d3[1]), re.sub(r"\s", "", d4[0]):re.sub(r"\s", "", d4[1])}
            col.insert_one(dict)
       
        elif detail6 == None:
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            d3 = detail3.text.strip().split("\n",1)
            d4 = detail4.text.strip().split("\n",1)
            d5 = detail5.text.strip().split("\n",1)
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))
            print(d3[0], re.sub(r"\s", "", d3[1]))
            print(d4[0], re.sub(r"\s", "", d4[1]))
            print(d5[0], re.sub(r"\s", "", d5[1]))
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1]),re.sub(r"\s", "", d3[0]):re.sub(r"\s", "", d3[1]), re.sub(r"\s", "", d4[0]):re.sub(r"\s", "", d4[1]), re.sub(r"\s", "", d5[0]):re.sub(r"\s", "", d5[1])}
            col.insert_one(dict)
      
        elif detail7 == None:
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            d3 = detail3.text.strip().split("\n",1)
            d4 = detail4.text.strip().split("\n",1)
            d5 = detail5.text.strip().split("\n",1)
            d6 = detail6.text.strip().split("\n",1)
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))
            print(d3[0], re.sub(r"\s", "", d3[1]))
            print(d4[0], re.sub(r"\s", "", d4[1]))
            print(d5[0], re.sub(r"\s", "", d5[1]))
            print(d6[0], re.sub(r"\s", "", d6[1]))
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1]),re.sub(r"\s", "", d3[0]):re.sub(r"\s", "", d3[1]), re.sub(r"\s", "", d4[0]):re.sub(r"\s", "", d4[1]), re.sub(r"\s", "", d5[0]):re.sub(r"\s", "", d5[1]), re.sub(r"\s", "", d6[0]):re.sub(r"\s", "", d6[1])}
            col.insert_one(dict)

        elif detail8 == None:
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            d3 = detail3.text.strip().split("\n",1)
            d4 = detail4.text.strip().split("\n",1)
            d5 = detail5.text.strip().split("\n",1)
            d6 = detail6.text.strip().split("\n",1)
            d7 = detail7.text.strip().split("\n",1)
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))
            print(d3[0], re.sub(r"\s", "", d3[1]))
            print(d4[0], re.sub(r"\s", "", d4[1]))
            print(d5[0], re.sub(r"\s", "", d5[1]))
            print(d6[0], re.sub(r"\s", "", d6[1]))
            print(d7[0], re.sub(r"\s", "", d7[1]))
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1]),re.sub(r"\s", "", d3[0]):re.sub(r"\s", "", d3[1]), re.sub(r"\s", "", d4[0]):re.sub(r"\s", "", d4[1]), re.sub(r"\s", "", d5[0]):re.sub(r"\s", "", d5[1]), re.sub(r"\s", "", d6[0]):re.sub(r"\s", "", d6[1]), re.sub(r"\s", "", d7[0]):re.sub(r"\s", "", d7[1])}
            col.insert_one(dict)
     
        elif detail9 == None:
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            d3 = detail3.text.strip().split("\n",1)
            d4 = detail4.text.strip().split("\n",1)
            d5 = detail5.text.strip().split("\n",1)
            d6 = detail6.text.strip().split("\n",1)
            d7 = detail7.text.strip().split("\n",1)
            d8 = detail8.text.strip().split("\n",1)
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))
            print(d3[0], re.sub(r"\s", "", d3[1]))
            print(d4[0], re.sub(r"\s", "", d4[1]))
            print(d5[0], re.sub(r"\s", "", d5[1]))
            print(d6[0], re.sub(r"\s", "", d6[1]))
            print(d7[0], re.sub(r"\s", "", d7[1]))
            print(d8[0], re.sub(r"\s", "", d8[1]))
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1]),re.sub(r"\s", "", d3[0]):re.sub(r"\s", "", d3[1]), re.sub(r"\s", "", d4[0]):re.sub(r"\s", "", d4[1]), re.sub(r"\s", "", d5[0]):re.sub(r"\s", "", d5[1]), re.sub(r"\s", "", d6[0]):re.sub(r"\s", "", d6[1]), re.sub(r"\s", "", d7[0]):re.sub(r"\s", "", d7[1]), re.sub(r"\s", "", d8[0]):re.sub(r"\s", "", d8[1])}
            col.insert_one(dict)
   
        else:
            print( "번호:", x ,"캠프이름: ", camp_name.text.strip())
            d1 = detail1.text.strip().split("\n",1)
            d2 = detail2.text.strip().split("\n",1)
            d3 = detail3.text.strip().split("\n",1)
            d4 = detail4.text.strip().split("\n",1)
            d5 = detail5.text.strip().split("\n",1)
            d6 = detail6.text.strip().split("\n",1)
            d7 = detail7.text.strip().split("\n",1)
            d8 = detail8.text.strip().split("\n",1)
            d9 = detail9.text.strip().split("\n",1)
            print(d1[0], re.sub(r"\s", " ", d1[1]))
            print(d2[0], re.sub(r"\s", "", d2[1]))
            print(d3[0], re.sub(r"\s", "", d3[1]))
            print(d4[0], re.sub(r"\s", "", d4[1]))
            print(d5[0], re.sub(r"\s", "", d5[1]))
            print(d6[0], re.sub(r"\s", "", d6[1]))
            print(d7[0], re.sub(r"\s", "", d7[1]))
            print(d8[0], re.sub(r"\s", "", d8[1]))
            print(d9[0], re.sub(r"\s", "", d9[1]))
            dict = {"_id":x,"캠프이름":re.sub(r"\s", "", camp_name.text),re.sub(r"\s", "", d1[0]):re.sub(r"\s", " ", d1[1]),re.sub(r"\s", "", d2[0]):re.sub(r"\s", "", d2[1]),re.sub(r"\s", "", d3[0]):re.sub(r"\s", "", d3[1]), re.sub(r"\s", "", d4[0]):re.sub(r"\s", "", d4[1]), re.sub(r"\s", "", d5[0]):re.sub(r"\s", "", d5[1]), re.sub(r"\s", "", d6[0]):re.sub(r"\s", "", d6[1]), re.sub(r"\s", "", d7[0]):re.sub(r"\s", "", d7[1]), re.sub(r"\s", "", d8[0]):re.sub(r"\s", "", d8[1]),re.sub(r"\s", "", d9[0]):re.sub(r"\s", "", d9[1])}
            col.insert_one(dict)

           
