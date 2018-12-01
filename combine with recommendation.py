import os
import math
import requests
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox

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

        window.wm_title("Travel Assistant")
        self.current_row=0

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
        list_=["Distance","Rank"]
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
        self.quit_button=tk.Button(window, text="Quit")
        self.quit_button.configure(command=quit)
        self.quit_button.grid(row=self.current_row, column=1, columnspan=1)
        self.current_row+=1

    
        

    def fetch(self):
        #create local variable
        home=self.home_text.get()
        home=self.get_lat_lng(home)
        time=self.duration_text.get()

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

        print(self.recommendation(self.df, home, place_have_been, preference, sort, duration = time))
    
        

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
    
    #exclude attractions that visitors has been before    
        i=0
        while i < len(visited):
            df = df[ ~ df['attraction'].str.contains(visited[i]) ]
            i += 1 
        df_1 = df#df_1 now is the dataframe without rows whose name is in visited list

    
        df_2 = df_1[df_1['type'].isin(preference)]#df_2 now is the dataframe only with rows whose 'type' is in preference list
        df_2['distance'] = df_2.apply(lambda x: self.get_distance(x['location']),axis = 1)
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
    def get_distance(self,location, startpoint):
            startpoint_x = startpoint_location[0]
            startpoint_y = startpoint_location[1]
            return math.sqrt(pow(location[0] - startpoint_x, 2)+ pow(location[1]- startpoint_y, 2))

            
#define main class implement execution loop
def main():
    window=tk.Tk()
    start=App(window)
    window.mainloop()

#run the main function
if __name__=="__main__":
    main()

