import requests
from bs4 import BeautifulSoup
import datetime
raw_data_list = list()
url = "https://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html#ATTRACTION_SORT_WRAPPER"
response = requests.get(url)
if not response.status_code == 200:
    raise NameError('Something wrong with the scraping process!')
results_page = BeautifulSoup(response.content,'lxml')
next_page_url = "https://www.tripadvisor.com" + results_page.find('div',class_="unified pagination ").find('a').get('href')
while (next_page_url != None):
    attraction_table = results_page.find('div',class_="attraction_list attraction_list_short ")
    attractions = table.find_all('div',class_="attraction_element")
    for attraction in attractions:
        attraction_link = "https://www.tripadvisor.com" + attraction.find('a').get('href')
        attraction_name = attraction.find('a').get_text()
        attraction_rate = attraction.find('div',class_="rs rating").find('span').get('alt').split( )[0]
        attraction_type = attraction.find('span',class_="matchedTag noTagImg").get_text()
        raw_data_list.append((attraction_link,attraction_name,attraction_rate,attraction_type))
        if results_page.find('div',class_="unified pagination ").find('a').get('href')
        next_page_url = "https://www.tripadvisor.com" + results_page.find('div',class_="unified pagination ").find('a').get('href')

url1 = "https://www.tripadvisor.com/Attraction_Review-g60763-d267031-Reviews-Manhattan_Skyline-New_York_City_New_York.html"
response1 = requests.get(url1)
if not response1.status_code == 200:
    print('Fail')
	
results_page1 = BeautifulSoup(response1.content,'lxml')
times = results_page1.find('span',class_="is-hidden-mobile header_detail")
times = times.find_all('span',class_="time")
open_time = list()
for time in times:
    temp = time.get_text().split( )[0]
    temp = datetime.datetime.strptime(temp,'%I:%M')
    open_time.append(temp)