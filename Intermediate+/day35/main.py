import os,requests
from dotenv import load_dotenv
load_dotenv()
WEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("WEATHER_API_KEY")

request_params = {
    'lat': os.getenv('MY_LATITUDE'),
    'lon': os.getenv('MY_LONGITUDE'),
    'appid': API_KEY,
    'cnt': 4, #intervalos de 3 horas a serem enviados
}
will_rain = False
response = requests.get(WEATHER_ENDPOINT,params=request_params)
response.raise_for_status()
weather_data = response.json()
#############################################################

for hourly_data in weather_data['list']:
    if (hourly_data['weather'][0]['id']) < 700:
        will_rain = True

print(f'Vai chover? {will_rain}')
