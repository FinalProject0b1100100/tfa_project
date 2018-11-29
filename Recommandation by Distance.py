
# coding: utf-8

# In[7]:


# use google API to transform the locaiton into a string, which represents the longitude and latitude
import math
import numpy as np
from pandas import DataFrame
import pandas as pd

class Recommandation:
    def __init__(self, visited, df):
        self.visited = visited
        self.df = df
        
    #exclude places that visitors has been before    
    def places_visited(self): #input a string recording the visited places
        i = 0
        for i< len(visited):
            self.df_1 = df[(True - self.df['attraction'].isin([visited[i]]))]
            i += 1

    #prefrence is the first criterion
    def rank_preference(self, preference):#input a string representing the preference  
    #   return aqicsv[(dataframe["characteristic"] = preference) output is the preference related dataframe
        self.preference = preference
        self.df_2 = df.loc[df['column_name'].isin(preference)] #!!!!!column_name here is is to be substitute!!!!!!!!
        
    #distance is the second criterion      
    def rank_distance(self, location):#input the string which represents the longitude and latitude
        self.location = location
        i= 0
        location_x = self.location[0]
        location_y = self.location[1]
        self.distance = {}
        self.attraction_pick = {}
    
        #to calculate distance between hotel and attraction
        for i < 50: #the total number of attractions is 50
            self.attraction_x = self.df_2[i, longitude] #extract the longitude
            self.attraction_y = self.df_2[i, latitude] #extract the latitude
            self.distance[{self.df_2[i,attraction]}] = 1 + math.sqrt(pow(self.location_x - self.attraction_x, 2) + pow(self.location_y - self.attraction_y, 2)) #+1 is to avoid 0
            i += 1
        
        #create a new dict called 'self.distance_sort' to deposite sorted dict
        self.distance_sort = sorted(self.distance.items(), key=lambda d: d[1], reverse=True) 
        return self.distance_sort
      
        #extract the top 5 attractions by distance
        count = 0
        for key, value in self.distance_sort:
            count += 1
            self.attraction_pick[key] = value
            return self.attraction_pick
        if count >= 5:
            break

    
    
    


# In[ ]:


#calculate time duration to derive the number of places to visit
class Sum_duration(Recommandation):
    def __init__(self, duration, df):
        self.duration = duration
        super().__init__(df)

    def sum_time(self):
        n = 0
        sum_time = 0
        name = list(self.distance_sort.keys())#extract the name of sorted attractions
        if sum_time < self.duration:
            time = df.loc[name[n],"time"]#extract time of the corresponding attractions
            sum_time = sum_time + time
            n += 1
        return n

