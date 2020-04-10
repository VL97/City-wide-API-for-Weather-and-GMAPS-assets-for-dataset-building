import requests
import pandas as pd 
from datetime import date
import os.path

  
def APIresponse():
    
    #Openweather api 
    api_key=PUT_API_KEY_HERE
    url = 'http://api.openweathermap.org/data/2.5/weather?q=bangalore&appid='+api_key

    #Required parameters for dataset. The JSON dictionary from API response also has the same named keys. 
    reqd_keys=sorted(['humidity', 'pressure' , 'temp_min', 'temp_max'])

    try:

        #GET api and extract json response
        response = requests.get(url)
        res_dic=response.json()['main']

        #keys in json response
        response_keys=list(res_dic.keys())

        #Filters unwanted data from response json
        for item in response_keys:
            if item not in reqd_keys:
                del res_dic[item]

        #final list of keys in filtered response
        final_keys=sorted(list(res_dic.keys()))

        #Checks if each of reqd keys match the final keys in filtered response
        for i in range(len(reqd_keys)):
            if(reqd_keys[i]!=final_keys[i]):
                raise Exception

    except:
        raise Exception("OpenWeather API response error.")
        
    #returned data dictionary to be added to dataset
    return res_dic


def newDataframe():
    
    #create a new dataframe table named 'weather.csv'
    df_new = pd.DataFrame(columns = ['pressure', 'humidity' , 'temp_min', 'temp_max', 'Date']) 
    df_new.to_csv('weather.csv',index=False) 
    
def addtoDataframe(data):

    #current date formatting
    dt=date.today()
    date_str=dt.strftime("%d/%m/%Y")
    #add date to data dictionary
    data['Date']=date_str

    #open 'weather.csv' append data and save
    df_read = pd.read_csv("weather.csv") 
    df_read=df_read.append(data, ignore_index=True, sort=None)
    df_read.to_csv('weather.csv',index=False) 

      
def main():

    #create 'weather.csv' if not present in current working directory
    if not (os.path.isfile("weather.csv")):
        newDataframe()
    
    #get data from server
    data_dict=APIresponse()
    #write data to csv
    addtoDataframe(data_dict)

    
#RUN
main()
