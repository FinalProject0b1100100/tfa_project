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
# exmple : get_map('Museum of Modern Art',df)


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
import networkx as nxt
%matplotlib inline
G_C=nx.Graph()
node_labels=dict()
nodes = list()

# example: startpoint = 'Mona Museum New York'
df1 = df['attraction']
df1[len(df)] = startpoint

for n in df1:
    nodes.append(n)

distances = [(df1[i],df1[j],get_distance_duration(df1[i],df1[j],api_key)[0]) for i in range(len(nodes)-1) for j in range(i+1,len(nodes))]    
    
for e in distances:
    G_C.add_edge(e[0],e[1],distance=e[2])

pos=nx.spring_layout(G_C) # positions for all nodes
# nodes
nx.draw_networkx_nodes(G_C,pos,
                       node_color='r',
                       node_size=500,
                      alpha=0.8)
# edges
#nx.draw_networkx_edges(sub_graph,pos,width=1.0,alpha=0.5)
nx.draw_networkx_edges(G_C,pos,
                       edgelist=G_C.edges(),
                       width=8,alpha=0.5,edge_color='b')
node_name={}
for node in G_C.nodes():
    node_name[node]=str(node)
nx.draw_networkx_edge_labels(G_C,pos,font_size=10)
node_name={}
for node in G_C.nodes():
    node_name[node]=str(node)
nx.draw_networkx_labels(G_C,pos,node_name,font_size=8)
plt.axis('off')
plt.show() # display

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
result = results[0]
