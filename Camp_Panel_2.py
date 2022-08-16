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
    # 2474 문제 있는 url이어서 pass
    if x == 2474:
        continue
    
    base_url = "https://www.gocamping.or.kr/bsite/camp/info/read.do?c_no="+str(x)+"&viewType=read01&listOrdrTrget=frst_register_pnttm"
    response = requests.get(base_url)
    source = response.text
    soup = BeautifulSoup(source, "lxml")
    
    # 캠프 이름
    camp_name = soup.find("p", class_="camp_name")
    # Panel2 - option 1
    detail1 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(1) > th")
    detail1_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(1) > td")

    # Panel2 - option 2
    detail2 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(2) > th")
    detail2_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(2) > td")

    # Panel2 - option 3
    detail3 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(3) > th")
    detail3_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(3) > td")

    # Panel2 - option 4
    detail4 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(4) > th")
    detail4_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(4) > td")

    # Panel2 - option 5
    detail5 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(5) > th")
    detail5_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(5) > td")

    # Panel2 - option 6
    detail6 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(6) > th")
    detail6_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(6) > td")

    # Panel2 - option 7
    detail7 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(7) > th")
    detail7_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(7) > td")

    # Panel2 - option 8
    detail8 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(8) > th")
    detail8_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(8) > td")

    # Panel2 - option 9
    detail9 = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(9) > th")
    detail9_sub = soup.select_one("#table_type03 > div > table > tbody > tr:nth-child(9) > td")

    info = soup.select_one("#cont_inner > div.sub_layout.layout > article > header > div > div.cont_tb > table") # 1번째 문단

    if info == None:
        print("페이지 없음", x)
        pass
    else:
        if detail1_sub == None and detail3_sub == None and detail4_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(re.sub(r"\s", "", detail2.text), re.sub(r"\s", " ", detail2_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail2.text):detail2_sub.text.strip()}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)
        elif detail1_sub == None and detail4_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(re.sub(r"\s", "", detail2.text), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip())}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)
        elif detail4_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(re.sub(r"\s", "", detail1.text), re.sub(r"\s", " ", detail1_sub.text.strip()))
            print(detail2.text.strip(), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail1.text):re.sub(r"\s", " ", detail1_sub.text.strip()), re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip())}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)
        elif detail5_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(detail1.text.strip(), re.sub(r"\s", " ", detail1_sub.text.strip()))
            print(detail2.text.strip(), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            print(detail4.text.strip(), re.sub(r"\s", " ", detail4_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail1.text):re.sub(r"\s", " ", detail1_sub.text.strip()), re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip()), re.sub(r"\s", "", detail4.text):detail4_sub.text.strip()}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)
        elif detail6_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(detail1.text.strip(), re.sub(r"\s", " ", detail1_sub.text.strip()))
            print(detail2.text.strip(), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            print(detail4.text.strip(), re.sub(r"\s", " ", detail4_sub.text.strip()))
            print(detail5.text.strip(), re.sub(r"\s", " ", detail5_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail1.text):re.sub(r"\s", " ", detail1_sub.text.strip()), re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip()), re.sub(r"\s", "", detail4.text):detail4_sub.text.strip(), re.sub(r"\s", "", detail5.text):detail5_sub.text.strip()}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)
        elif detail7_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(detail1.text.strip(), re.sub(r"\s", " ", detail1_sub.text.strip()))
            print(detail2.text.strip(), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            print(detail4.text.strip(), re.sub(r"\s", " ", detail4_sub.text.strip()))
            print(detail5.text.strip(), re.sub(r"\s", " ", detail5_sub.text.strip()))
            print(detail6.text.strip(), re.sub(r"\s", " ", detail6_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail1.text):re.sub(r"\s", " ", detail1_sub.text.strip()), re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip()), re.sub(r"\s", "", detail4.text):detail4_sub.text.strip(), re.sub(r"\s", "", detail5.text):detail5_sub.text.strip(), re.sub(r"\s", "", detail6.text):detail6_sub.text.strip()}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)
        elif detail8_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(detail1.text.strip(), re.sub(r"\s", " ", detail1_sub.text.strip()))
            print(detail2.text.strip(), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            print(detail4.text.strip(), re.sub(r"\s", " ", detail4_sub.text.strip()))
            print(detail5.text.strip(), re.sub(r"\s", " ", detail5_sub.text.strip()))
            print(detail6.text.strip(), re.sub(r"\s", " ", detail6_sub.text.strip()))
            print(detail7.text.strip(), re.sub(r"\s", " ", detail7_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail1.text):re.sub(r"\s", " ", detail1_sub.text.strip()), re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip()), re.sub(r"\s", "", detail4.text):detail4_sub.text.strip(), re.sub(r"\s", "", detail5.text):detail5_sub.text.strip(), re.sub(r"\s", "", detail6.text):detail6_sub.text.strip(), re.sub(r"\s", "", detail7.text):detail7_sub.text.strip()}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)
        elif detail9_sub == None:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(detail1.text.strip(), re.sub(r"\s", " ", detail1_sub.text.strip()))
            print(detail2.text.strip(), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            print(detail4.text.strip(), re.sub(r"\s", " ", detail4_sub.text.strip()))
            print(detail5.text.strip(), re.sub(r"\s", " ", detail5_sub.text.strip()))
            print(detail6.text.strip(), re.sub(r"\s", " ", detail6_sub.text.strip()))
            print(detail7.text.strip(), re.sub(r"\s", " ", detail7_sub.text.strip()))
            print(detail8.text.strip(), re.sub(r"\s", " ", detail8_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail1.text):re.sub(r"\s", " ", detail1_sub.text.strip()), re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip()), re.sub(r"\s", "", detail4.text):detail4_sub.text.strip(), re.sub(r"\s", "", detail5.text):detail5_sub.text.strip(), re.sub(r"\s", "", detail7.text):detail6_sub.text.strip(), re.sub(r"\s", "", detail7.text):detail7_sub.text.strip(), re.sub(r"\s", "", detail8.text):re.sub(r"\s", " ", detail8_sub.text.strip())}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)      
        else:
            print( "번호:", x ,"캠프 이름:",camp_name.text.strip())
            print(detail1.text.strip(), re.sub(r"\s", " ", detail1_sub.text.strip()))
            print(detail2.text.strip(), re.sub(r"\s", " ", detail2_sub.text.strip()))
            print(detail3.text.strip(), re.sub(r"\s", " ", detail3_sub.text.strip()))
            print(detail4.text.strip(), re.sub(r"\s", " ", detail4_sub.text.strip()))
            print(detail5.text.strip(), re.sub(r"\s", " ", detail5_sub.text.strip()))
            print(detail6.text.strip(), re.sub(r"\s", " ", detail6_sub.text.strip()))
            print(detail7.text.strip(), re.sub(r"\s", " ", detail7_sub.text.strip()))
            print(detail8.text.strip(), re.sub(r"\s", " ", detail8_sub.text.strip()))
            print(detail9.text.strip(), re.sub(r"\s", " ", detail9_sub.text.strip()))
            dict = {re.sub(r"\s", "", detail1.text):re.sub(r"\s", " ", detail1_sub.text.strip()), re.sub(r"\s", "", detail2.text):re.sub(r"\s", " ", detail2_sub.text.strip()), re.sub(r"\s", "", detail3.text):re.sub(r"\s", " ", detail3_sub.text.strip()), re.sub(r"\s", "", detail4.text):detail4_sub.text.strip(), re.sub(r"\s", "", detail5.text):detail5_sub.text.strip(), re.sub(r"\s", "", detail6.text):detail6_sub.text.strip(), re.sub(r"\s", "", detail7.text):detail7_sub.text.strip(), re.sub(r"\s", "", detail8.text):re.sub(r"\s", " ", detail8_sub.text.strip()), re.sub(r"\s", "", detail9.text):detail9_sub.text.strip()}
            col.update_one({"_id":x}, {"$set":dict}, upsert=True)    
            
        
           
