
# coding: utf-8

# In[ ]:


# read data from recommendation 
df = self.recommendation(self.df, home, place_have_been, preference, sort, duration = time)

# create a function to get the address of a place in details, refer to couese material in Data Analytics
def get_address(address_string,api_key):
    response_data = get_location_data(address_string+'New York')
    return response_data['results'][0]['formatted_address']
# example: get_address("Columbia University",api_key)


# apply former function into data sample
df['address'] = df.apply(lambda x: get_address(x['attraction'],api_key),axis=1)


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


# create a network map with the distance between two point as edges
# refer to course material in DATA ANALYTICS
import networkx as nx
get_ipython().magic('matplotlib inline')
G_C=nx.Graph()
node_labels=dict()
nodes = list()

# example: startpoint = 'Museum of modern art'
df1 = df['attraction']
df1[len(df)] = startpoint

for n in df1:
    nodes.append(n)

distances = [(df1[i],df1[j],get_distance_duration(df1[i],df1[j],api_key)[0]) for i in range(len(nodes)-1) for j in range(i+1,len(nodes))]    
    
for e in distances:
    G_C.add_edge(e[0],e[1],distance=e[2])

#create a dictionary containing the distance between each place
distances2 = [((df1[i],df1[j]),get_distance_duration(df1[i],df1[j],api_key)[0]) for i in range(len(nodes)) for j in range(len(nodes)) if j!=i]
dict_=dict(distances2)
# find all the ways visiting from startpoint and formulating a circle
results = list()
for y in df['attraction']:
    for x in list(nx.all_simple_paths(G_C,startpoint,y)):
        if len(x) == len(df1):
            path_len = get_distance_duration(startpoint,y,api_key)[0]
            for i in range(len(df1)-1):
                path_len += dict_[(x[i],x[i+1])]
            results.append((x,round(path_len,2)))
results = sorted(results,key = lambda x: x[1])

## result!
route = results[0][0]
distance_total = results[0][1]

## edges of the result
route_edges = [(route[i],route[i+1]) for i in range(len(route)-1)]
route_edges.append((route[-1],route[0]))

# get all information about starting point and attractions
# click the icon and you will get all information
df2 = df
df2 = df2.append([{'attraction':startpoint,'lat':get_lat_lng(startpoint,api_key)[0],'lng':get_lat_lng(startpoint,api_key)[1]}], ignore_index=True)
def get_map(startpoint,result):
    import folium
    import os
    startpoint_ll = get_lat_lng(startpoint,api_key)
    m = folium.Map(location=startpoint_ll,zoom_start=14)
    icon_hz = dict(prefix='fa', color='red', icon_color='darkred', icon='cny')
    folium.Marker(startpoint_ll, popup = startpoint,icon=folium.Icon(color='green')).add_to(m)
    for i in range(len(df)):
            folium.Marker([df.iloc[i]['lat'],df.iloc[i]['lng']],
                            popup='Attraction: '+df.iloc[i]['attraction']+ ';   Address: '+df.iloc[i]['address']
                          + ';   Duration: ' +str(df.iloc[i]['duration'])+' hour(s);   Type: ' +df.iloc[i]['type']
                          + ';   Link: ' +df.iloc[i]['attraction_link']
                             ).add_to(m)
    for i in route_edges:
        lat1 = df2[df2['attraction']==i[0]]['lat'].iloc[0]
        lng1 = df2[df2['attraction']==i[0]]['lng'].iloc[0]
        lat2 = df2[df2['attraction']==i[1]]['lat'].iloc[0]
        lng2 = df2[df2['attraction']==i[1]]['lng'].iloc[0]
        ls = folium.PolyLine(locations=[[lat1,lng1],[lat2,lng2]],color='blue')
        ls.add_to(m)
    return m
# get_map(startpoint,df2)

