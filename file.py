#version 1
import requests
api_key = 'AIzaSyAVBY1Pfw6KcKxr-1fQzHlGDnD7q_L9CBg'
address="Grand Army Plaza"
address=address.replace(' ','_')
url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address,api_key)
response = requests.get(url)
response.json()
