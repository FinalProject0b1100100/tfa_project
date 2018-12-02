## Path Planner: Your Best Travel Partner in the City of New York :statue_of_liberty:     
#### 4501 Final Project from Group 0b1100100  
  
  
### What is it?   
---
**Path Planner** is a graphical user interface to design the sightseeing routes for tourists. 
After some basic settings like your `current location` and `travel preferences`, 
you will see our **designed route** in **blue line** and **suggested attractions** in **blue pins** shown in the real map.  
We believe our plan would match you perfectly based on our sufficient data fetched from **Tripadvisor** and we have prepared top `71` attractions in New York City which can definitly meet all your travel needs!

### Who are we?  :two_women_holding_hands::two_women_holding_hands:
---
|Name|UNI|Section|
|---|---|---|
|Qinya Li|ql2333|Section002|
|Yanghuizi Wang|yw3189|Section002|
|Weiyi Huang|wh2422|Section002|
|Luokun Ren|lr2897|Section002|

### How to play with it? :video_game:    
---
#### Installation Instructions :ledger:  
After reading this [Requirements](https://github.com/FinalProject0b1100100/tfa_project/blob/master/Requirements.txt) :page_with_curl:, you are ready to go!  

#### Click [final project.ipynb](https://github.com/FinalProject0b1100100/tfa_project/blob/master/final%20project.ipynb) :open_file_folder:  
Download this file and open it in Jupyter Notebook.  
You can run it with the data and libraries you have downloaded as the [Requirements](https://github.com/FinalProject0b1100100/tfa_project/blob/master/Requirements.txt) instructed.
After clicking, a pop-up will display in your desktop. :newspaper:  

#### Input Setting :inbox_tray:
- [x] Your API key: This is the API key described in the Requirements.(**Required**)   
- [x] Your hotel address: This is the start point of your day trip and is necessary. It can be your current location or the future hotel location in your plan.(**Required**)    
- [x] Duration: Please input your estimated play time and this is the pure sightviewing time without transportation.(**Required**) 
- [ ]  Please select the attractions that you have visited before, and you can select none or more than one.  
- [ ]  Please select your preferred type of attractions, and you can select noen or more than one. 
- [x]  Please choose your priority when picking attarctions.(**Required**)    

#### For example  
If you were the `first time` been New York City, and you started from `Columbia University`.   
You are an enthusiastic `art fan` and you want to vist some famous `museums`.  
After enjoying the art, you want to experience the `neighborhood`.
Your estimated playing time is around `6` hours.  
And you want to firstly visit the attractions which is nearst to you.
![The example input](https://raw.githubusercontent.com/FinalProject0b1100100/tfa_project/master/input1.png)  
![The example input](https://raw.githubusercontent.com/FinalProject0b1100100/tfa_project/master/input2.png)  

#### Press the OK botton and return to [final project.ipynb](https://github.com/FinalProject0b1100100/tfa_project/blob/master/final%20project.ipynb) 
Please wait a minute for the perfect path we designed for you!  
    
### What you will see? :outbox_tray:    
---
First you will see the table showing the detailed inforamtion of the selected attractions！
![The example output](https://raw.githubusercontent.com/FinalProject0b1100100/tfa_project/master/output1.jpg) 

Still no idea about where they are? :astonished:   

Don't worry, we have prepared a map for you! :sunglasses: 

It just takes some time, let's wait for the magic! :sparkles:   

![The example output](https://raw.githubusercontent.com/FinalProject0b1100100/tfa_project/master/output2.jpg)  

Your start point is shown by green point :herb:  
The route is represented by blue lines :wavy_dash:  
The attractions that we have picked for you is shown by blue pins :small_blue_diamond:  

What's more, considerable as we are, if you click the blue pins, you will see the detail information of the attarctions like name, address, suggested viewing time and the type.  

### How to reset it?   
---
If you want to use it again and we believe you will, just stop the origin kernal, close the previous pop-up and restart the kernal to plan your path again.  

## Now let's try it and travel the New York City :sunrise: :mount_fuji: :rainbow: :stars:    

### Appendix  
|File Name|Description|
|---|---|
|Recommendation by Distance.py|This file reads the data file and stores it as a pandas data frame. Then it deletes the visited attractions obtained from input from the data frame and select the recommeded attractions by sorting preference with the summation of all duration is under the duration constraint obtained from input |
|Scraping Part.py|This file is used to obtain the raw data from website|
|Combine with Recommendation.py|The file has both GUI and recommendation files and is able to pass the input obtained from GUI and return the recommendation table at the end|
|data_with_location.csv|The data set that contains all useful information(name, type, rank, duration, latitude and longitude, etc.) of each attration in NYC|
|File.py|This file defines functions to get Google Map by API and plan the ordered path between each location. It also has functions to display the information and pin of the location from the data frame|
|Final Project.py|Python file version of the completed project. It is able to take input from GUI, get the recommend attrations, and plot the on the Google Map with travel details|
|Final Project.ipynb|Jupter notebook file version of the completed project|


