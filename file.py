import requests
# try to find the latitude and longitude of a place
# refer to couese material in Data Analytics
# api_key can't be posed in github

# create a function to get the latitude and longitude of a place
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
# example: get_lat_lng("Columbia University",api_key)

# create a function to get the address of a place in details
def get_address(address_string,api_key):
    response_data = get_location_data(address_string+'New York')
    return response_data['results'][0]['formatted_address']
# example: get_address("Columbia University",api_key)


# create imaginary sample data (since the data from web crawler part is not accessible now)
import pandas as pd
df = pd.DataFrame({'attraction':['Columbia University','Manhattan Skyline','Time Square','Central Park'],'price':[1,2,1,3]})
# apply former function into data sample
df['lat'] = df.apply(lambda x: get_lat_lng(x['attraction'],api_key)[0],axis=1)
df['lng'] = df.apply(lambda x: get_lat_lng(x['attraction'],api_key)[1],axis=1)
df['address'] = df.apply(lambda x: get_address(x['attraction'],api_key),axis=1)


# create a function to get a map of the result
import folium
def get_map(startpoint,result):
    startpoint = get_lat_lng(startpoint,api_key)
    m = folium.Map(location=startpoint,zoom_start=14)
    for i in range(len(df)):
        folium.Marker([df.iloc[i]['lat'],df.iloc[i]['lng']],popup=df.iloc[i]['attraction']).add_to(m)
    return m
# exmple : get_map('Mona museum',df)


# create a function to get distance and duration from one place to another place
def get_distance_duration(origin,destination,api_key):
    
    result = list()
    origin = origin.replace(' ','+')
    destination = destination.replace(' ','+')
    url= "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s" % (origin, destination, api_key)
    try:
        response = requests.get(url)
        if not response.status_code == 200:
            print("HTTP error",response.status_code)
        else:
            try: 
                distance = response.json()['routes'][0]['legs'][0]['distance']['text'].split()[0]
                duration = response.json()['routes'][0]['legs'][0]['duration']['text'].split()[0]
                return (float(distance),float(duration))
            except:
                print("Response not in valid JSON format")
    except:
        print("Something went wrong with requests.get")
## example :get_distance_duration('Columbia university','time squre',api_key)
