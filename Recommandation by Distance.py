
# coding: utf-8

# In[1]:


# import all the libraries
import pandas as pd
import math

df = pd.read_csv("data_with_location.csv", index_col = 0)
# check the dataframe
# df.head()

df = df.rename(index=str, columns={"attraction_name": "attraction", "attraction_type": "type", "attraction_rank": "rank", "attraction_duration": "duration", "attraction_lat": "lat", "attraction_lng": "lng"})

# combine lat and lng as 'location' and add to the dataframe
loc = list()
for i in range(len(df)):
    a = df['lat'][i]
    b = df['lng'][i]
    loc.append((a, b))
df['location'] = loc

# check the dataframe
# df.head()

# use google API to transform the locaiton into a string, which represents the longitude and latitude
import requests
api_key = 'AIzaSyAcJo9m6XPc5L32vRt6BXTfeXdVxw81n78'

# get_location
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

# get _lat_lng
def get_lat_lng(address_string,api_key):
    response_data = get_location_data(address_string+'New York')
    return (response_data['results'][0]['geometry']['location']['lat'],
           response_data['results'][0]['geometry']['location']['lng'])

# these are continued to be substituted
startpoint = 'museum of modern art'
startpoint_location =  get_lat_lng(startpoint,api_key)
visited = ['Central Park']
preference = ['Park','Museum']
duration = 4
priority = 'distance'

def recommendation(df, startpoint, visited, preference, priority, duration = 24):
    #startpoint is a string usually recording the hotel's longtitude and latitude
    #visited is a string recording where you have been
    #preference is a string representing the type of attractions that you want to visit
    #priority is crorder by rank or distance
    #duration is the upper time limit of all selected attractions
    
    #exclude attractions that visitors has been before    
    i=0
    while i < len(visited):
        df = df[ ~ df['attraction'].str.contains(visited[i]) ]
        i += 1 
    df_1 = df#df_1 now is the dataframe without rows whose name is in visited list

    
    df_2 = df_1[df_1['type'].isin(preference)]#df_2 now is the dataframe only with rows whose 'type' is in preference list
      
    #get the x & y of startpoint
    startpoint_x = startpoint_location[0]
    startpoint_y = startpoint_location[1]

    #add the distance between startpoint and attractions as 'distance' to df_2
    def get_distance(location):
        return math.sqrt(pow(location[0] - startpoint_x, 2)+ pow(location[1]- startpoint_y, 2))
    df_2['distance'] = df_2.apply(lambda x: get_distance(x['location']),axis = 1)
    
    #When sorting by distance, ascending. When sorting by rank, descending.
    df_3 = df_2.sort_values(by=priority,ascending=(priority=='distance')) # df_3 now is the sorted dataframe by priority('distance' or 'rank')

    #calculate time duration to derive the number of places to visit
    n = 0
    sum_time = 0

    # extract the name of sorted attractions
    while (sum_time < duration) & (n < len(df_3)):
        time = df_3.iloc[n]['duration'] # extract time of the corresponding attractions
        sum_time += time
        n += 1
    
    result = df_3.iloc[:n-1]
    result = result.reset_index(drop = True)
    return result
# r = recommendation (df, startpoint_location, visited, preference, priority, duration)

