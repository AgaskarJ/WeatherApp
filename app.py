from flask import Flask, render_template, request, redirect, url_for
import requests, json
import pandas as pd
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Global dictionaries 
weather_info = {}
historical_info = {}

# Main index 
@app.route('/', methods=['GET', 'POST'])
def index():
    
    api_key = "ea09906907113e49377962ba6ac8334a"
    city_name = request.form.get("city")
    # Current weather end point
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_key}'
    response = requests.get(base_url).json()
 
    # On success code
    if response['cod'] == 200: 

        # Current Weather
        weather_info['Temperature'] = round((response['main']['temp'] - 273.15) * (9/5) + 32,2) 
        weather_info['Feels Like'] = round((response['main']['feels_like'] - 273.15) * (9/5) + 32,2)
        weather_info['City'] = response['name']
        # Coordinates declared as variables for historical weather use
        lat = response['coord']['lat']
        lon = response['coord']['lon'] 
        weather_info['Latitude'] = lat
        weather_info['Longitude'] = lon
        weather_info['Main Weather'] = response['weather'][0]['main']
        weather_info['Description'] = response['weather'][0]['description']
        time = response['dt']

        flag = response['sys']['country'].lower()
        icon_id = response['weather'][0]['icon'] # Get icon image as png
        icon_url = f'http://openweathermap.org/img/w/{icon_id}.png'

        # Historical Weather
        # 5 API calls per historical day. Day 1: 
        historical_time = timeCalc(time)
        date_1 = datetime.utcfromtimestamp(historical_time[0]).strftime('%m-%d-%Y')
        historical_info['Date1'] = date_1
        hist_1 = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={historical_time[0]}&appid={api_key}&only_current=True'
        hist_resp_1 = requests.get(hist_1).json()
        historical_info['Temperature1'] = round((hist_resp_1['current']['temp'] - 273.15) * (9/5) + 32,2)
        historical_info['Feels Like1'] = round((hist_resp_1['current']['feels_like'] - 273.15) * (9/5) + 32,2)
        historical_info['Main Weather1'] = hist_resp_1['current']['weather'][0]['main']
        historical_info['Description1'] = hist_resp_1['current']['weather'][0]['description']
        hist_icon_1 = hist_resp_1['current']['weather'][0]['icon']
        historical_info['Icon1'] = f'http://openweathermap.org/img/w/{hist_icon_1}.png'

        # Day 2: 
        date_2 = datetime.utcfromtimestamp(historical_time[1]).strftime('%m-%d-%Y')
        historical_info['Date2'] = date_2
        hist_2 = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={historical_time[1]}&appid={api_key}&only_current=True'
        hist_resp_2 = requests.get(hist_2).json()
        historical_info['Temperature2'] = round((hist_resp_2['current']['temp'] - 273.15) * (9/5) + 32,2)
        historical_info['Feels Like2'] = round((hist_resp_2['current']['feels_like'] - 273.15) * (9/5) + 32,2)
        historical_info['Main Weather2'] = hist_resp_2['current']['weather'][0]['main']
        historical_info['Description2'] = hist_resp_2['current']['weather'][0]['description']
        hist_icon_2 = hist_resp_2['current']['weather'][0]['icon']
        historical_info['Icon2'] = f'http://openweathermap.org/img/w/{hist_icon_2}.png'

        # Day 3: 
        date_3 = datetime.utcfromtimestamp(historical_time[2]).strftime('%m-%d-%Y')
        historical_info['Date3'] = date_3
        hist_3 = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={historical_time[2]}&appid={api_key}&only_current=True'
        hist_resp_3 = requests.get(hist_3).json()
        historical_info['Temperature3'] = round((hist_resp_3['current']['temp'] - 273.15) * (9/5) + 32,2)
        historical_info['Feels Like3'] = round((hist_resp_3['current']['feels_like'] - 273.15) * (9/5) + 32,2)
        historical_info['Main Weather3'] = hist_resp_3['current']['weather'][0]['main']
        historical_info['Description3'] = hist_resp_3['current']['weather'][0]['description']
        hist_icon_3 = hist_resp_3['current']['weather'][0]['icon']
        historical_info['Icon3'] = f'http://openweathermap.org/img/w/{hist_icon_3}.png'

        # Day 4: 
        date_4 = datetime.utcfromtimestamp(historical_time[3]).strftime('%m-%d-%Y')
        historical_info['Date4'] = date_4
        hist_4 = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={historical_time[3]}&appid={api_key}&only_current=True'
        hist_resp_4 = requests.get(hist_4).json()
        historical_info['Temperature4'] = round((hist_resp_4['current']['temp'] - 273.15) * (9/5) + 32,2)
        historical_info['Feels Like4'] = round((hist_resp_4['current']['feels_like'] - 273.15) * (9/5) + 32,2)
        historical_info['Main Weather4'] = hist_resp_4['current']['weather'][0]['main']
        historical_info['Description4'] = hist_resp_4['current']['weather'][0]['description']
        hist_icon_4 = hist_resp_4['current']['weather'][0]['icon']
        historical_info['Icon4'] = f'http://openweathermap.org/img/w/{hist_icon_4}.png'

        # Day 5: 
        date_5 = datetime.utcfromtimestamp(historical_time[4]).strftime('%m-%d-%Y')
        historical_info['Date5'] = date_5
        hist_5 = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={historical_time[4]}&appid={api_key}&only_current=True'
        hist_resp_5 = requests.get(hist_5).json()
        historical_info['Temperature5'] = round((hist_resp_5['current']['temp'] - 273.15) * (9/5) + 32,2)
        historical_info['Feels Like5'] = round((hist_resp_5['current']['feels_like'] - 273.15) * (9/5) + 32,2)
        historical_info['Main Weather5'] = hist_resp_5['current']['weather'][0]['main']
        historical_info['Description5'] = hist_resp_5['current']['weather'][0]['description']
        hist_icon_5 = hist_resp_5['current']['weather'][0]['icon']
        historical_info['Icon5'] = f'http://openweathermap.org/img/w/{hist_icon_5}.png'

        # Calculate metrics
        historical_info['Average'] = round((historical_info['Temperature1'] + historical_info['Temperature2'] + historical_info['Temperature3'] 
                        + historical_info['Temperature4'] + historical_info['Temperature5'])/5,2)
        historical_info['Delta'] = round(((weather_info['Temperature'] - historical_info['Temperature5'])/historical_info['Temperature5']) * 100,2)

        # Displays static map image using MapBox API
        map_api_key = 'pk.eyJ1IjoiYWdhc2thcmoiLCJhIjoiY2w0bHl2eHYzMDJvcjNubzIwNXZudjRzYSJ9.tfQhaNmHNWn9j9eJHedfAQ'
        map_url = f'https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/{lon},{lat},13/1280x1000?access_token={map_api_key}'

        return render_template("index.html", weather_info=weather_info, icon_url=icon_url, 
        historical_info=historical_info, response=response, hist_resp_1=hist_resp_1, hist_resp_2=hist_resp_2, 
        hist_resp_3=hist_resp_3, hist_resp_4=hist_resp_4, hist_resp_5=hist_resp_5, flag=flag, map_url=map_url)
    else: 
        return "City is not found!"

# Calculates Unix time for the past five days 
# Returns a list of unix time
def timeCalc(time): 
    list = []
    for i in range(1,6):  
        list.append(time - (86400 * i))
    return list
    
# Download dataframe to excel
# Currently saves into project folder 
# Further TO DO: Excel formatting - transpose dataframe
@app.route('/download_excel')
def download_excel():
    df1 = pd.DataFrame(weather_info, index=['Current']) #.transpose()
    df2 = pd.DataFrame(historical_info, index=['Historical']) #.transpose()
    with pd.ExcelWriter("output.xlsx") as writer:
        df1.to_excel(writer, sheet_name="Current", index=False)
        df2.to_excel(writer, sheet_name="Historical", index=False)
    
if __name__ == "__main__":
    app.run(debug=True)

