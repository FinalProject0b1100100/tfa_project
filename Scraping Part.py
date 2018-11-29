# Necessary Libraries
import requests
from bs4 import BeautifulSoup
import datetime

# Link for attractions in tripadvisor
url = "https://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html#ATTRACTION_SORT_WRAPPER"

def get_attractions(url):
    
    # Put all summarized data of attractions from the summary page
    raw_data_list = list()
    response = requests.get(url)
    
    # Check if scraping the page successfully
    if not response.status_code == 200:
        raise NameError('Something wrong with the scraping process!')
        
    results_page = BeautifulSoup(response.content,'lxml')
    
    # First page of the attractions has different tags and structures from other pages
    # This unexpected change started at 11/29/2018
    # Thus the info from first page should be scraped separately
    attraction_table = results_page.find('div', class_="ui_container attractions-attraction-overview-main-TopPOIs__container--1-Iay")
    attraction = attraction_table.find_all('li', class_="attractions-attraction-overview-main-TopPOIs__item--e3w3i")
    for attraction in attractions:
        attraction_link = "https://www.tripadvisor.com" + attraction.find('a').get('href')
        attraction_name = attraction.find('a').get_text()
        attraction_rating = attraction.find('div',class_="ui_poi_review_rating").find('span')['class'][1][7:]
        attraction_type = attraction.find('span',class_="attractions-commerce-CategoryTag__category_tag--9vIyT").get_text()
        raw_data_list.append((attraction_link,attraction_name,attraction_rate,attraction_type))
     
    # Obtain link for next_page in page 1
    next_page_url = "https://www.tripadvisor.com" + results_page.find('div',class_="attractions-attraction-overview-main-Pagination__link--2F1AA   ui_button primary attractions-attraction-overview-main-Pagination__button--1Nc9C").find('a').get('href')

    # For every page, do the loop to get link, name, rating and type of attractions
    while (next_page_url != None):
        attraction_table = results_page.find('div',class_="attraction_list attraction_list_short ")
        attractions = attraction_table.find_all('div',class_="attraction_element")
        for attraction in attractions:
            attraction_link = "https://www.tripadvisor.com" + attraction.find('a').get('href')
            attraction_name = attraction.find('a').get_text()
            attraction_rating = attraction.find('div',class_="rs rating").find('span').get('alt').split( )[0]
            attraction_type = attraction.find('span',class_="matchedTag noTagImg").get_text()
            raw_data_list.append((attraction_link,attraction_name,attraction_rate,attraction_type))
            
            # Obtain next_page in all other pages until no page left
            try:
                next_page_url = "https://www.tripadvisor.com" + results_page.find('div',class_="unified pagination ").find('a').get('href')
            except:
                next_page_url = None
    # return all info of attractions
    return raw_data_list





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