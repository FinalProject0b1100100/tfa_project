import requests
# try to find the latitude and longitude of a place
# refer to couese material in Data Analytics
api_key = 'AIzaSyAcJo9m6XPc5L32vRt6BXTfeXdVxw81n78')
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
# create a function to get the address of a place in details
def get_address(address_string,api_key):
    response_data = get_location_data(address_string+'New York')
    return response_data['results'][0]['formatted_address']
get_address("Columbia University",api_key)
# create imaginative sample data (since the data from web crawler part is not accessible now)
import pandas as pd
df = pd.DataFrame({'attraction':['Columbia University','Manhattan Skyline'],'price':[1,2]})
  

