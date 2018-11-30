
# coding: utf-8

# In[1]:


df = pd.DataFrame({'attraction':['Columbia University','Manhattan Skyline','Time Square','Central Park','Soho'],'duration':[1,2,3,4,5],'rank':[4.3,4.5,3.9,4.4,4.8],'type':['University','Skyscraper','Square','Park','Shopping']})
import requests
api_key = 'AIzaSyAcJo9m6XPc5L32vRt6BXTfeXdVxw81n78'
def get_location_data(address):
    response_data = ''
    url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address,api_key)
    try:
        response = requests.get(url)
        if not response.status_code == 200:
            print("HTTP error",response.status_code)
        else:
            try:
                response_data = response.json()
            except:
                print("Response not in valid JSON format")
    except:
        print("Something went wrong with requests.get")
    return response_data
def get_lat_lng(address_string,api_key):
    response_data = get_location_data(address_string+'New York')
    return (response_data['results'][0]['geometry']['location']['lat'],
           response_data['results'][0]['geometry']['location']['lng'])

df['location'] = df.apply(lambda x: get_lat_lng(x['attraction'],api_key),axis=1)
startpoint = 'museum of modern art'
startpoint_ll =  get_lat_lng(startpoint,api_key)
visited = ['Columbia University']
preference = ['Shopping','Park','Square']
duration = 9
city_pass = 1
priority = 'distance'

import math
import pandas as pd


def recommendation(df, startpoint, visited, preference, duration = 24, price):
    #startpoint is a string usually recording the hotel's location
    #visited is a string recording where you have been 
    #preference is a string representing the type of attractions you want to visited
    #duration is the upper time limit of all selected attractions
    #price is the ticket fee for attarctions
    
    #exclude attractions that visitors has been before    
    i=0
    while i < len(visited):
        df = df[ ~ df['attraction'].str.contains(visited[i]) ]
        i += 1 
    df_1 = df#df_1 now is the dataframe without rows whose name is in visited list
    
    #prefrence is the first criterion
    df_2 = df_1[df_1['type'].isin(preference)]#df_2 now is the dataframe only with rows whose 'type' is in preference list 
    
    #distance is the second criterion   
    #get the x & y of startpoint
    startpoint_x = startpoint[0]
    startpoint_y = startpoint[1]

    #add the distance between startpoint and attractions as 'distance' to df_2
    def get_distance(x):
        return math.sqrt(pow(x[0] - startpoint_x, 2)+ pow(x[1]- startpoint_y, 2))
    df_2['distance'] = df_2.apply(lambda x: get_distance(x['location']),axis = 1)
    df_3 = df_2.sort_values(by='distance') # df_3 now is the sorted dataframe by 'distance'
    
    #calculate time duration to derive the number of places to visit
    n = 0
    sum_time = 0
    while sum_time < duration & n < len(df_3):
        time = df_3.iloc[n]['duration']#extract time of the corresponding attractions
        sum_time =+ time
        n += 1
    
    result = df_3.iloc[:n-1]
    return result

