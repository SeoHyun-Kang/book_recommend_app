from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import csv

url = 'https://book.naver.com/category/index.nhn?cate_code=180020&tab=top100&list_type=list&sort_type=publishday&page=5'
request = requests.get(url)
request.encoding = 'utf-8'
bs=BeautifulSoup(request.text,'html.parser')

category = [] #lc_100, lc_110 ..
category_name = [] #소설, 시/에세이
a = bs.find(id='left_category').find_all('a')

for i in range(len(a)):
  temp = a[i].get('name')
  if (temp):
    category.append(temp)
    category_name.append(a[i].span.string)

for i in range(len(category)):
  category[i] = category[i][3:]


s_sub_cat = []
s_sub_cat_name = []
for i in range(len(category)):  
  code = category[i]
  url = 'https://book.naver.com/category/index.nhn?cate_code={code}'.format(code = code)
  request = requests.get(url)
  request.encoding = 'utf-8'
  bs=BeautifulSoup(request.text,'html.parser')

  temp = bs.find_all(class_='category_detail_inner')
  
  for j in range(len(temp)): 
    temp2 = temp[j].find_all("a")
    for k in range(len(temp2)-1): # 1부터 마지막 원소까지 돌아야함
      s_sub_cat.append(temp2[k+1].get("href"))
      s_sub_cat_name.append(temp2[k+1].string) #가장 하위 카테고리 이름


# 메타 정보와 본문에서 필요한 정보를 추출합니다.
# csv 파일에 각 정보 저장 w:새로 만들기 a:기존 파일에 append
file = open('bookdb_8.csv','a',encoding='utf-8', newline='')
csvfile = csv.writer(file)
# csvfile.writerow(["분야","분야 내 카테고리","서브 카테고리","순위", "책이름", "저자", "줄거리","이미지"])

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)

# driver.get('https://www.naver.com/')
# time.sleep(1)

# # 로그인 버튼을 찾고 클릭합니다
# login_btn = driver.find_element_by_class_name('link_login')
# login_btn.click()
# time.sleep(1)

# # id, pw 입력할 곳을 찾습니다.
# tag_id = driver.find_element_by_name('id')
# tag_pw = driver.find_element_by_name('pw')
# tag_id.clear()
# time.sleep(1)

# # id 입력
# tag_id.click()
# pyperclip.copy('아이디')
# tag_id.send_keys(Keys.CONTROL, 'v')
# time.sleep(1)

# # pw 입력
# tag_pw.click()
# pyperclip.copy('비번#')
# tag_pw.send_keys(Keys.CONTROL, 'v')
# time.sleep(1)

# # 로그인 버튼을 클릭합니다
# login_btn = driver.find_element_by_id('log.login')
# login_btn.click()

i=368
for code in s_sub_cat[368:]:
  print (f"현재 코드: {code} 카테고리 이름: {s_sub_cat_name[i]}")
  i+=1
  for page in range(1,6):
    url = code+'&tab=top100&list_type=list&sort_type=publishday&page={page}'.format(page=page)

    # 네이버의 베스트셀러 웹페이지 정보
    driver.get(url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')

    # 책의 상세 웹페이지 주소를 추출하여 리스트에 저장
    book_page_urls = []

    for index in range(0, 20):
      dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
      if dl_data==None or dl_data.find('img',{'class':"adult"}) : #성인 인증 도서
            break #건너뛰기
      link = dl_data.select('a')[0].get('href')
      book_page_urls.append(link)

    # 메타 정보와 본문에서 필요한 정보를 추출합니다.
    # csv 파일에 각 정보 저장
    # file = open('test.csv','a',encoding='utf8', newline='')
    # csvfile = csv.writer(file)
    
    #카테고리 정보 가져오는 부분
    field = bsObject.find(class_='select').a.string
    sub_field = bsObject.find(class_='select2').a.string
    if (bsObject.find(class_='select3')):
        sub_sub_field = bsObject.find(class_='select3').a.string
    else:
        sub_sub_field = "."

    #리스트로 받아온 책의 각 세부 url 안에 들어가서 순위, 제목, 저자, 이미지, 책내용 받아오기
    for index, book_page_url in enumerate(book_page_urls):
      driver.get(book_page_url)

      bsObject = BeautifulSoup(driver.page_source, 'html.parser')
             
      title = bsObject.find('meta', {'property':'og:title'}).get('content')
      image = bsObject.find('meta', {'property':'og:image'}).get('content')
      description = bsObject.find('meta', {'property' : 'og:description'}).get('content')
      url = bsObject.find('meta', {'property':'og:url'}).get('content')
      try:
        author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
      except:
        author = '저자정보없음'
      dd = bsObject.find('dt', text='가격').find_next_siblings('dd')[0]

      
      csvfile.writerow([field, sub_field, sub_sub_field, 20*(page-1)+index+1, title, author, description, image])

file.close()
    