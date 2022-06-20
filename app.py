from flask import Flask, render_template, request, redirect, url_for
import requests, json
import pandas as pd

app = Flask(__name__)

#global dictionaries 
weather_info = {}
historical_info = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    
    api_key = "ea09906907113e49377962ba6ac8334a"

    city_name = request.form.get("city")
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_key}'
    response = requests.get(base_url).json()
 
    if response['cod'] == 200: #if success code run get
        weather_info['Temperature'] = round((response['main']['temp'] - 273.15) * (9/5) + 32,2) #convert temp to Farenheit
        weather_info['Feels Like'] = round((response['main']['feels_like'] - 273.15) * (9/5) + 32,2)
        weather_info['City'] = response['name']
        lat = response['coord']['lat']
        lon = response['coord']['lon'] 
        weather_info['Latitude'] = lat
        weather_info['Longitude'] = lon
        weather_info['Main Weather'] = response['weather'][0]['main']
        weather_info['Description'] = response['weather'][0]['description']

        icon_id = response['weather'][0]['icon'] #get icon image as png
        icon_url = f'http://openweathermap.org/img/w/{icon_id}.png'

        time = 1655614800 #Unix time for historical weather 06/19/2022
        historical_url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={api_key}'
        hist_response = requests.get(historical_url).json()
        historical_info['Temperature'] = round((hist_response['current']['temp'] - 273.15) * (9/5) + 32,2)
        historical_info['Feels Like'] = round((hist_response['current']['feels_like'] - 273.15) * (9/5) + 32,2)
        historical_info['Main Weather'] = hist_response['current']['weather'][0]['main']
        historical_info['Description'] = hist_response['current']['weather'][0]['description']
        hist_icon_id = hist_response['current']['weather'][0]['icon']
        hist_icon_url = f'http://openweathermap.org/img/w/{hist_icon_id}.png'

        map_api_key = 'pk.eyJ1IjoiYWdhc2thcmoiLCJhIjoiY2w0bHl2eHYzMDJvcjNubzIwNXZudjRzYSJ9.tfQhaNmHNWn9j9eJHedfAQ'
        map_url = f'https://api.mapbox.com/styles/v1/mapbox/outdoors-v11/static/{lon},{lat},13/1280x1000?access_token={map_api_key}'

        return render_template("index.html", weather_info=weather_info, icon_url=icon_url, 
        historical_info=historical_info, hist_icon_url=hist_icon_url, response=response, hist_response=hist_response, map_url=map_url)
    else: 
        return "City is not found!"

@app.route('/download_excel')
def download_excel():
    df1 = pd.DataFrame(weather_info, index=['Current']) #.transpose()
    df2 = pd.DataFrame(historical_info, index=['Historical']) #.transpose()
    with pd.ExcelWriter("output.xlsx") as writer:
        df1.to_excel(writer, sheet_name="Current", index=False)
        df2.to_excel(writer, sheet_name="Historical", index=False)

if __name__ == "__main__":
    app.run(debug=True)

