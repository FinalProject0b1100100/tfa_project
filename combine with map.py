import os
import math
import requests
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox
# create a network map with the distance between two point as edges
# refer to course material in DATA ANALYTICS
import folium
import networkx as nx

class App(object):
    df=pd.read_csv("data_with_location.csv", index_col=0)
    df = df.rename(index=str, columns={"attraction_name": "attraction", "attraction_type": "type", "attraction_rank": "rank", "attraction_duration": "duration", "attraction_lat": "lat", "attraction_lng": "lng"})

    # combine lat and lng as 'location' and add to the dataframe
    loc = list()
    for i in range(len(df)):
        a = df['lat'][i]
        b = df['lng'][i]
        loc.append((a, b))
    df['location'] = loc
    df.drop(columns = ['attraction_rating'])
    
    list_=df['type'].unique()
    att_list=df['attraction']
    attration=[]
    pref_list=[]
    for x in list_:
        pref_list.append(x)
    for x in att_list:
        attration.append(x)
    
    #pref_list=["Shopping", "Event", "Museum", "Park"]
    #attration=["Central Park", "5th ave", "Chinatown", "St Patrick Church"]
    phb_list=[]
    var_list=[]  #for preference use
    api_key = 'AIzaSyAcJo9m6XPc5L32vRt6BXTfeXdVxw81n78'
    
    def __init__(self, window):

        window.wm_title("Path Planner")
        self.current_row=0
        
        #api key
        self.api_label=tk.Label(window,text="Your API key:")
        self.api_label.grid(row=self.current_row, column=0)
        self.api_text=tk.StringVar()
        self.api_entry=tk.Entry(window, textvariable=self.api_text)
        self.api_entry.grid(row=self.current_row, column=1)
        self.current_row+=1
        
        # Hotel address
        self.home_label=tk.Label(window,text="Your hotel address:")
        self.home_label.grid(row=self.current_row, column=0)
        self.home_text=tk.StringVar()
        self.home_entry=tk.Entry(window, textvariable=self.home_text)
        self.home_entry.grid(row=self.current_row, column=1)
        self.current_row+=1

        #duration
        self.duration_label=tk.Label(window,text="Your everyday travel duration is:")
        self.duration_label.grid(row=self.current_row, column=0)
        self.duration_text=tk.DoubleVar()
        self.duration_text=tk.IntVar()
        self.duration_entry=tk.Entry(window, textvariable=self.duration_text)
        self.duration_entry.grid(row=self.current_row, column=1)
        self.current_row+=1
        
        #place have been 
        self.phb_label=tk.Label(window,text="Places that you have been to:")
        self.phb_label.grid(row=self.current_row, column=0)
        self.phb_entry=  Menubutton (window, text="Please select all", relief=RAISED )
        self.phb_entry.grid(row=self.current_row, column=1)
        self.phb_entry.menu  =  Menu ( self.phb_entry, tearoff = 0 )
        self.phb_entry["menu"]  =  self.phb_entry.menu
        for x in range(len(self.attration)):
            x=IntVar()
            self.phb_list.append(x)
        for x in range(len(self.attration)):
            self.phb_entry.menu.add_checkbutton ( label=self.attration[x],variable=self.phb_list[x])
        self.current_row+=1    

        #preference
        self.preference_label=tk.Label(window,text="Attraction type preference:")
        self.preference_label.grid(row=self.current_row, column=0)
        self.preference_entry=  Menubutton (window, text="Please select all", relief=RAISED )
        self.preference_entry.grid(row=self.current_row, column=1)
        self.preference_entry.menu  =  Menu ( self.preference_entry, tearoff = 0 )
        self.preference_entry["menu"]  =  self.preference_entry.menu
        #list_=["Shopping", "Event", "Museum", "Park"]
        for x in range(len(self.pref_list)):
            var=IntVar()
            self.var_list.append(var)
        for x in range(len(self.pref_list)):
            self.preference_entry.menu.add_checkbutton ( label=self.pref_list[x],variable=self.var_list[x])
        self.current_row+=1 
        
        #sort
        self.sort_label=tk.Label(window,text="Sort by:")
        self.sort_label.grid(row=self.current_row, column=0)
        #####----------change this-----------####
        list_=["distance","rank"]
        self.sort_text=StringVar()
        self.sort_entry=OptionMenu(window, self.sort_text, *list_)
        self.sort_entry.grid(row=self.current_row, column=1)
        self.current_row+=1
        self.current_row+=1

        #OK button
        self.query_button=tk.Button(window, text="OK")
        self.query_button.configure(command=self.fetch)
        self.query_button.grid(row=self.current_row, column=0, columnspan=1)
        
        #quit button
        self.quit_button=tk.Button(window, text="Cancel")
        self.quit_button.configure(command=quit)
        self.quit_button.grid(row=self.current_row, column=1, columnspan=1)
        self.current_row+=1
       

    def fetch(self):
        #create local variable
        home=self.home_text.get()
        time=self.duration_text.get()
        
        #realize storing api_key later
        api_key=self.api_text.get()

        #place_have_been
        place_have_been=[]
        for x in range(len(self.phb_list)):
            if self.phb_list[x].get()==1:
                place_have_been.append(self.attration[x])

        #preference
        preference=[]
        for x in range(len(self.pref_list)):
            if self.var_list[x].get()==1:
                preference.append(self.pref_list[x])
                
        #citypass=self.cp_text.get()
        sort=self.sort_text.get()
        
        dff=self.recommendation(self.df, home, place_have_been, preference, sort, duration = time)
        dff['address'] = dff.apply(lambda x: self.get_address(x['attraction']),axis=1)
        
        get_ipython().magic('matplotlib inline')
        G_C=nx.Graph()
        node_labels=dict()
        nodes = list()

        # example: startpoint = 'Museum of modern art'
        dff1 = dff['attraction']
        dff1[len(dff)] = home

        for n in dff1:
            nodes.append(n)

        distances = [(dff1[i],dff1[j],self.get_distance_duration(dff1[i],dff1[j],self.api_key)[0]) for i in range(len(nodes)-1) for j in range(i+1,len(nodes))]    
    
        for e in distances:
            G_C.add_edge(e[0],e[1],distance=e[2])

        #create a dictionary containing the distance between each place
        distances2 = [((dff1[i],dff1[j]),self.get_distance_duration(dff1[i],dff1[j],self.api_key)[0]) for i in range(len(nodes)) for j in range(len(nodes)) if j!=i]
        dict_=dict(distances2)
        # find all the ways visiting from startpoint and formulating a circle
        results = list()
        for y in dff['attraction']:
            for x in list(nx.all_simple_paths(G_C,home,y)):
                if len(x) == len(dff1):
                    path_len = self.get_distance_duration(home,y,self.api_key)[0]
                    for i in range(len(dff1)-1):
                        path_len += dict_[(x[i],x[i+1])]
                    results.append((x,round(path_len,2)))
        results = sorted(results,key = lambda x: x[1])

        ## result!
        route = results[0][0]
        distance_total = results[0][1]

        ## edges of the result
        route_edges = [(route[i],route[i+1]) for i in range(len(route)-1)]
        route_edges.append((route[-1],route[0]))

        dff2 = dff
        dff2 = dff2.append([{'attraction':home,'lat':self.get_lat_lng(home)[0],'lng':self.get_lat_lng(home)[1]}], ignore_index=True)
        
        display(self.get_map(home,dff,dff2, route_edges))

    def get_map(self,startpoint,dff,dff2, route_edges):
        startpoint_ll = self.get_lat_lng(startpoint)
        m = folium.Map(location=startpoint_ll,zoom_start=14)
        icon_hz = dict(prefix='fa', color='red', icon_color='darkred', icon='cny')
        folium.Marker(startpoint_ll, popup = startpoint,icon=folium.Icon(color='green')).add_to(m)
        for i in range(len(dff)):
                folium.Marker([dff.iloc[i]['lat'],dff.iloc[i]['lng']],
                            popup='Attraction: '+dff.iloc[i]['attraction']+ ';   Address: '+dff.iloc[i]['address']
                          + ';   duration: ' +str(dff.iloc[i]['duration'])+';   type: ' +dff.iloc[i]['type']
                          + ';   link: ' +dff.iloc[i]['attraction_link']
                             ).add_to(m)
        for i in route_edges:
            lat1 = dff2[dff2['attraction']==i[0]]['lat'].iloc[0]
            lng1 = dff2[dff2['attraction']==i[0]]['lng'].iloc[0]
            lat2 = dff2[dff2['attraction']==i[1]]['lat'].iloc[0]
            lng2 = dff2[dff2['attraction']==i[1]]['lng'].iloc[0]
            ls = folium.PolyLine(locations=[[lat1,lng1],[lat2,lng2]],color='blue')
            ls.add_to(m)
        return m
    
    # get_location
    def get_location_data(self, address):
        response_data = ''
        url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (address,self.api_key)
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
        """this method and api_key is never used """
    def get_lat_lng(self,address_string):
        response_data = self.get_location_data(address_string+'New York')
        return (response_data['results'][0]['geometry']['location']['lat'], response_data['results'][0]['geometry']['location']['lng'])

    def recommendation(self, df, startpoint, visited, preference, priority, duration = 24):
    #startpoint is a string usually recording the hotel's longtitude and latitude
    #visited is a string recording where you have been
    #preference is a string representing the type of attractions that you want to visit
    #priority is crorder by rank or distance
    #duration is the upper time limit of all selected attractions
        startpoint_location=self.get_lat_lng(startpoint)
        #exclude attractions that visitors has been before    
        i=0
        while i < len(visited):
            df = df[ ~ df['attraction'].str.contains(visited[i]) ]
            i += 1 
        df_1 = df#df_1 now is the dataframe without rows whose name is in visited list

    
        df_2 = df_1[df_1['type'].isin(preference)]#df_2 now is the dataframe only with rows whose 'type' is in preference list
        df_2['distance'] = df_2.apply(lambda x: self.get_distance(x['location'], startpoint_location),axis = 1)
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
    
    #get the x & y of startpoint
    def get_distance(self,location, startpoint_location):
            startpoint_x = startpoint_location[0]
            startpoint_y = startpoint_location[1]
            return math.sqrt(pow(location[0] - startpoint_x, 2)+ pow(location[1]- startpoint_y, 2))
    
    def get_address(self,address_string):
        response_data = self.get_location_data(address_string+'New York')
        return response_data['results'][0]['formatted_address']    
    
    
    # create a function to get distance and duration from one place to another place
    def get_distance_duration(self,origin,destination,api_key):    
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

            
#define main class implement execution loop
def main():
    window=tk.Tk()
    start=App(window)
    window.mainloop()
#run the main function
if __name__=="__main__":
    main()




