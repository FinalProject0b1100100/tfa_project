
# coding: utf-8

# In[8]:


# use google API to transform the locaiton into a string, which represents the longitude and latitude
import math
import numpy as np
from pandas import DataFrame
import pandas as pd

class Recommandation:
    def __init__(self, visited, df):
        self.visited = visited
        self.df = df
        
    #exclude attractions that visitors has been before    
    def places_visited(self): #input a string recording the visited places
        i = 0
        while i< len(visited):
            self.df_1 = df[(True - self.df['attraction'].isin([visited[i]]))] #df_1 now is the dataframe without rows whose name is in visited list
            i += 1

    #prefrence is the first criterion
    def rank_preference(self, preference):#input a string representing the preference  
    #   return aqicsv[(dataframe["characteristic"] = preference) output is the preference related dataframe
        self.preference = preference
        self.df_2 = df.loc[df['type'].isin(preference)] #df_2 now is the dataframe only with rows whose 'type' is in preference list
        
    #distance is the second criterion      
    def rank_distance(self, location):#input the string which represents the longitude and latitude
        self.location = location
        i= 0
        self.location_x = self.location[0]
        self.location_y = self.location[1]
#       self.distance = {}
    
        #to calculate distance between hotel and attraction
#         while i < len(self.df_2): #the total number of attractions is dataframe2
#             self.attraction_x = self.df_2.iloc[i]['longitude'] #extract the longitude
#             self.attraction_y = self.df_2.iloc[i]['latitude'] #extract the latitude
#             df_2['distance'] = pow(df_2['longitude']-self.location_x,2)+
#             self.distance[{self.df_2.loc[i]['attraction']}] = 1 + math.sqrt(pow(self.location_x - self.attraction_x, 2) + pow(self.location_y - self.attraction_y, 2)) #+1 is to avoid 0
#             i += 1
        
        #add the distance between hotel and attractions as 'distance' to df_2
        def get_distance(x):
            return pow(x[0]-self.location_x,2)+ pow(x[1]-self.location_y,2)
        self.df_2['distance'] = self.df_2.apply(lambda x: get_distance(x['location']),axis = 1)
        
        
        self.df_2.sort_values(by='distance')
        return self.df_2 #df_2 now is the sorted dataframe by distance

#calculate time duration to derive the number of places to visit
class Sum_duration(Recommandation):
    def __init__(self, duration):
        self.duration = duration

    def sum_time(self):
        n = 0
        sum_time = 0
        #extract the name of sorted attractions
        while sum_time < self.duration:
            time = self.df_2.iloc[n]['duration']#extract time of the corresponding attractions
            sum_time = sum_time + time
            n += 1
        return n
    

class Pick_attractions(Recommandation, Sum_duration):
    def pick(self):
        self.limit = super().sum_time
        
    
#       self.attraction_pick = {}
        
    #extract the top attractions by distance within time limit
    
        count = 0
        for key, value in self.distance_sort:
            count += 1
            self.attraction_pick[key] = value
            return self.attraction_pick
            if count >= self.limit:
                break


# In[20]:


import pandas as pd
df_2 = pd.DataFrame({'attraction':['Columbia University','Manhattan Skyline','Time Square','Central Park'],'location':[(30,34),(34,33),(40,32),(50,42)],'duration':[2,3,1,1]})


# In[24]:


location_x = 30
location_y = 20

def get_distance(x):
    return pow(x[0]-location_x,2)+ pow(x[1]-location_y,2)
df_2['distance'] = df_2.apply(lambda x: get_distance(x['location']),axis = 1)
df_2.sort_values(by='distance')
df_2


# In[17]:


df_2


# In[30]:


# use google API to transform the locaiton into a string, which represents the longitude and latitude
import math
import numpy as np
from pandas import DataFrame
import pandas as pd


def recommendation(df, startpoint, visited, preference, duration):
    #visited is a string recording the visited places 
    #preference is a string representing the preference
    #duration is the upper limit of all selected attractions
    
    #exclude attractions that visitors has been before    
    i = 0
    while i< len(visited):
        df_1 = df[(True - df['attraction'].isin([visited[i]]))] #df_1 now is the dataframe without rows whose name is in visited list
        i += 1

    #prefrence is the first criterion
    self.df_2 = df_1.loc[df['type'].isin(preference)] #df_2 now is the dataframe only with rows whose 'type' is in preference list
        
    #distance is the second criterion   
    #get the x & y of startpoint
    i= 0
    startpoint_x = startpoint[0]
    startpoint_y = startpoint[1]
        
    #add the distance between startpoint and attractions as 'distance' to df_2
    def get_distance(x):
        return 1 + math.sqrt(pow(x[0] - startpoint_x, 2)+ pow(x[1]- startpoint_y, 2))
    df_2['distance'] = df_2.apply(lambda x: get_distance(x['location']),axis = 1)        
    df_2.sort_values(by='distance') #df_2 now is the sorted dataframe by distance

    #calculate time duration to derive the number of places to visit
    n = 0
    sum_time = 0
    #extract the name of sorted attractions
    while sum_time < duration:
        time = self.df_2.iloc[n]['duration']#extract time of the corresponding attractions
        sum_time = sum_time + time
        n += 1
    
    #extract the top attractions by distance within time limit
    result = df_2.iloc[:n]


# In[31]:


recommendation(df,'Columbia University', ['a'], ['museum'], 10)

