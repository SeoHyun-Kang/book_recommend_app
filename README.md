# book_recommend_app
2021-1학기 졸업작품

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv


url = "https://book.naver.com/category/index.nhn?cate_code=100010&tab=top100&list_type=list&sort_type=publishday&page=1".format(code=code)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)


# 네이버의 베스트셀러 웹페이지 정보
driver.get(url)
bsObject = BeautifulSoup(driver.page_source, 'html.parser')



# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장
book_page_urls = []

for page in range(1,6):
    

    for index in range(0, 20):
        dl_data = bsObject.find('dt', {'id':"book_title_"+str(index)})
        link = dl_data.select('a')[0].get('href')
        book_page_urls.append(link)

# 메타 정보와 본문에서 필요한 정보를 추출합니다.
# csv 파일에 각 정보 저장
file = open('bookdb_소설_나라별.csv','w',encoding='cp949', newline='')
csvfile = csv.writer(file)
csvfile.writerow(["순위", "책이름", "저자", "줄거리","이미지"])

for index, book_page_url in enumerate(book_page_urls):
    
    driver.get(book_page_url)
    bsObject = BeautifulSoup(driver.page_source, 'html.parser')


    title = bsObject.find('meta', {'property':'og:title'}).get('content')
    author = bsObject.find('dt', text='저자').find_next_siblings('dd')[0].text.strip()
    image = bsObject.find('meta', {'property':'og:image'}).get('content')
    description = bsObject.find('meta', {'property' : 'og:description'}).get('content')
    url = bsObject.find('meta', {'property':'og:url'}).get('content')
    dd = bsObject.find('dt', text='가격').find_next_siblings('dd')[0]

    #print(index+1, title, author, image)
    
    csvfile.writerow([index+1, title, author, description, image])

file.close()
    




    
"""
    book_list[i].append = index+1
    book_list[i].append = title
    book_list[i].append = author
    book_list[i].append = image
    """
"""
def toCSV(book_list):

    file = open('bookdb_list.csv','w',encoding='cp949', newline='')
    csvfile = csv.writer(file)
    csvfile.writerow(["순위", "책이름", "저자", "이미지"])
    csvfile.writerow(booklist)

    for i in book_list:    
        csvfile.writerow(i)
    file.close()

toCSV(book_list)
"""
