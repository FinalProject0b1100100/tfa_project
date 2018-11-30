# Necessary Libraries
import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import csv

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
    attractions = attraction_table.find_all('li', class_="attractions-attraction-overview-main-TopPOIs__item--e3w3i")
    for attraction in attractions:
        attraction_link = "https://www.tripadvisor.com" + attraction.find('a',rel="noopener noreferrer").get('href')
        attraction_name = attraction.find('a',class_="attractions-attraction-overview-main-TopPOIs__name--3eQ8p").get_text()
        attraction_rating = int(attraction.find('div',class_="ui_poi_review_rating").find('span').get('class')[1][7:])/10
        attraction_type = attraction.find('span',class_="attractions-commerce-CategoryTag__category_tag--9vIyT").get_text()
        raw_data_list.append((attraction_name, attraction_link, attraction_rating, attraction_type))
        
    # Obtain link for next  ge in page 1
    next_page_url = "https://www.tripadvisor.com/Attractions-g60763-Activities-oa30-New_York_City_New_York.html"

    # For every page, do the loop to get link, name, rating and type of attractions
    # Since there are 38 pages of attractions in New York City, we think top 90 attractions will be enough to new tourists
    # which means we only need 3 pages of attractions
    page = 1
    while (page < 3):
        page += 1
        response = requests.get(next_page_url)
        
        # Check if scraping the page successfully
        if not response.status_code == 200:
            raise NameError(f'Something wrong with the scraping process for page {page}!')

        results_page = BeautifulSoup(response.content,'lxml')
        
        attraction_table = results_page.find('div',class_="attraction_list attraction_list_short ")
        attractions = attraction_table.find_all('div',class_="attraction_element")
        
        for attraction in attractions:
            attraction_link = "https://www.tripadvisor.com" + attraction.find('div',class_="listing_title ").find('a').get('href')
            attraction_name = attraction.find('div',class_="listing_title ").find('a').get_text()
            attraction_rating = float(attraction.find('div',class_="rs rating").find('span').get('alt').split( )[0])
            attraction_type = attraction.find('span',class_="matchedTag noTagImg").get_text()
            raw_data_list.append((attraction_name, attraction_link, attraction_rating, attraction_type))
        
        # Obtain the url of page 3 in page 2
        next_page_url = "https://www.tripadvisor.com/Attractions-g60763-Activities-oa30-New_York_City_New_York.html#FILTERED_LIST"
        
    # return all info of attractions
    return raw_data_list

# Get the raw data list
raw_data_list = get_attractions(url)

# Save the info of attractions as a csv file
raw_data = pd.DataFrame(raw_data_list, columns = ['attraction_name', 'attraction_link', 'attraction_rating', 'attraction_type'])
# raw_data.to_csv("raw_data_list.csv")
# raw_data = pd.read_csv()

# Data Clean -- Add rank for popularity
rank = range(1,91)
raw_data['attraction_rank'] = rank

# Data Clean -- Drop duplicated attraction_names and reset indexes
raw_data_1 = raw_data.drop_duplicates(subset = ['attraction_name'], keep = 'first')
raw_data_1=raw_data_1.reset_index(drop=True)

# Data Clean -- Re-classify attraction_types
# Check attraction_type
# raw_data_1['attraction_type'].unique()
raw_data_1['attraction_type'].value_counts()

# Classify those whose name and type has 'Museum' in it as 'Museum'
for i in range(len(raw_data_1)):
    if ('Museum' in raw_data_1['attraction_name'][i])|('Museums' in raw_data_1['attraction_type'][i]):
        raw_data_1['attraction_type'][i] = 'Museum'

raw_data_1

raw_data_1['attraction_type'].value_counts()



import requests
from bs4 import BeautifulSoup
import datetime
raw_data_list = list()
url = "https://www.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html#ATTRACTION_SORT_WRAPPER"
response = requests.get(url)
if not response.status_code == 200:
    raise NameError('Something wrong with the scraping process!')
results_page = BeautifulSoup(response.content,'lxml')
attraction_table = results_page.find('div',class_="attraction_list attraction_list_short ")
attractions = attraction_table.find_all('div',class_="attraction_element")
for attraction in attractions:
    attraction_link = "https://www.tripadvisor.com" + attraction.find('a').get('href')
    attraction_name = attraction.find('a').get_text()
    attraction_rate = attraction.find('div',class_="rs rating").find('span').get('alt').split( )[0]
    attraction_type = attraction.find('span',class_="matchedTag noTagImg").get_text()
    raw_data_list.append((attraction_link,attraction_name,attraction_rate,attraction_type))
    
raw_data_list



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

	
	
type(open_time[0])
