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

# Data Clean -- Drop duplicated attraction_names and reset indexes
raw_data_1 = raw_data.drop_duplicates(subset = ['attraction_name'], keep = 'first')
raw_data_1 = raw_data_1.reset_index(drop=True)

# Data Clean -- Re-classify attraction_types
# Check attraction_type
# raw_data_1['attraction_type'].unique()
# raw_data_1['attraction_type'].value_counts()

# Classify those whose name and type has 'Museum' in it as 'Museum'
for i in range(len(raw_data_1)):
    if ('Museum' in raw_data_1['attraction_name'][i])|('Museums' in raw_data_1['attraction_type'][i]):
        raw_data_1['attraction_type'][i] = 'Museum'

# Since Hasted Kraeutler Gallery has closed, we should exclud this place
raw_data_2 = raw_data_1[raw_data_1['attraction_type'] != 'Art Galleries']
# raw_data_2['attraction_type'].value_counts()

# Change the type "Sights & Landmarks","Points of Interest & Landmarks","Historic Sites" into "Landmarks"
raw_data_2.loc[raw_data_2['attraction_type'] == 'Sights & Landmarks', 'attraction_type'] = 'Landmark'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Points of Interest & Landmarks', 'attraction_type'] = 'Landmark'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Historic Sites', 'attraction_type'] = 'Landmark'
# raw_data_2['attraction_type'].value_counts()

# Change the type "Shopping", "Tramways" ,"Transportation", "Architectural Buildings" into "Landmarks"
raw_data_2.loc[raw_data_2['attraction_type'] == 'Shopping', 'attraction_type'] = 'Neighborhoods'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Tramways', 'attraction_type'] = 'Neighborhoods'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Transportation', 'attraction_type'] = 'Neighborhoods'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Architectural Buildings', 'attraction_type'] = 'Neighborhoods'
# raw_data_2['attraction_type'].value_counts()

# Classify all the arts entertainments as "Art"
raw_data_2.loc[raw_data_2['attraction_type'] == 'Theaters', 'attraction_type'] = 'Art'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Ballets', 'attraction_type'] = 'Art'
# raw_data_2['attraction_type'].value_counts()

# Classify the type "Gardens", "Nature & Parks" as "Parks"
raw_data_2.loc[raw_data_2['attraction_type'] == 'Gardens', 'attraction_type'] = 'Parks'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Nature & Parks', 'attraction_type'] = 'Parks'
# raw_data_2['attraction_type'].value_counts()

# Classify the type "Churches & Cathedrals", "Sacred & Religious Sites" as "Religious Sites"
raw_data_2.loc[raw_data_2['attraction_type'] == 'Churches & Cathedrals', 'attraction_type'] = 'Religious Sites'
raw_data_2.loc[raw_data_2['attraction_type'] == 'Sacred & Religious Sites', 'attraction_type'] = 'Religious Sites'
# raw_data_2['attraction_type'].value_counts()

# Since specific events only hold for specific seasons, we need to exclude them in our data list
raw_data_3 = raw_data_2[raw_data_2['attraction_type'] != 'Events']
raw_data_4 = raw_data_3[raw_data_3['attraction_type'] != 'Cultural Events']
# raw_data_2['attraction_type'].value_counts()

# Reset the index of the list
raw_data_4=raw_data_4.reset_index(drop=True)

# Add the popularity rank for all the locations in our list
# Since when we scrap the web page, the order is actually according to the popularity, we only need to number our list of locations
rank = range(1,len(raw_data_4) + 1)
raw_data_4['attraction_rank'] = rank

# Save the info of attractions as a csv file
raw_data = pd.DataFrame(raw_data_4, columns = ['attraction_name', 'attraction_link', 'attraction_rating', 'attraction_type', 'attraction_rank'])
# raw_data.to_csv("raw_data_clean.csv")
# raw_data_clean = pd.read_csv("raw_data_clean.csv", index_col=0)

# Get the duration of each attraction
list_ = list(raw_data_clean['attraction_link'])
n = len(list_)
res = list()
# Scrap duration for each link of attraction
for i in range(n):
    # Keep track of the scraping process
    # print(i)
    # Initialize duration as 0
    duration = 0
        
    url = list_[i]
    response = requests.get(url)
    # if not response.status_code == 200:
    #     raise NameError('Something wrong with the scraping process!')
    results_page = BeautifulSoup(response.content,'lxml')

    info_table = results_page.find('div', class_="attractions-attraction-detail-about-card-AttractionDetailAboutCard__aboutCardWrapper--2I_lX")
        
    # Check if there is a suggested duration on the website
    if info_table:
        info = info_table.find_all('div', class_="attractions-attraction-detail-about-card-AttractionDetailAboutCard__section--WwZwR")
        pattern = r'^Suggested duration'
        duration = 0
        for j in info:
            match = re.search(pattern, j.get_text())
            if match:
                duration = j.get_text()
    if duration:
        res.append(duration)
    # If there is no duration, count it as None
    else:
        res.append(None)
		
# Data Clean -- duration
raw_duration = list()
for i in range(len(res)):
    if res[i]:
        
        # If the duration offered as a range, we will take the average
        if re.search(r'-', res[i]):
            pattern = r'\d-\d'
            string = res[i]
            match = re.findall(pattern, string)
            a, b = match[0].split('-')
            raw_duration.append((int(b) + int(a))/2)
            
        # If the duration offered a specific hour, we will only take that number as the duration
        else:
            match = re.findall(r'\d', res[i])
            raw_duration.append(int(match[0]))
            
    # If no duration provided, we estimate the duration to be half an hour.
    else:
        raw_duration.append(0.5)

# Add duration to our info table
raw_data_clean['attraction_duration'] = raw_duration

# Save the final info as a csv file
raw_data_clean.to_csv("data.csv")

=======================================================================================================================================================
import pandas as pd

# Init dataframe
df = pd.read_csv("data.csv", index_col = 0)

# Function to get lat & lng of each attractions
def get_lat_lng(address_string,api_key):
    response_data = get_location_data(address_string+'New York')
    return (response_data['results'][0]['geometry']['location']['lat'],
           response_data['results'][0]['geometry']['location']['lng'])

list_ = df['attraction_name']
lat = list()
lng = list()
for i in range(len(list_)):
    print(i)
    # We use our own api key here
    location = get_lat_lng(list_[i], api_key)
    lat.append(location[0])
    lng.append(location[1])
    
# Add the lag & lng to our data table
df['attraction_lat'] = lat
df['attraction_lng'] = lng

# Save it to csv
df.to_csv("data_with_location.csv")