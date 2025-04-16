from dotenv import load_dotenv
import os, smtplib
from datetime import datetime
import requests #MODULO DE API's
load_dotenv()
my_lat = float(os.getenv("MY_LATITUDE"))
my_lgn = float(os.getenv("MY_LONGITUDE"))
#################################################Main Functions
def iss_tracker(): #funcao que calcula se a posicao da ISS esta proxima da posicao do USER
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status() #caso dê erro
    data = response.json()['iss_position']
    ISS_POS = (float(data['latitude']),float(data['longitude']))
    if (my_lat - 5)<ISS_POS[0]<(my_lat+5) and (my_lgn-5)<ISS_POS[1]<(my_lgn+5):
        print('its above')
        return True
    else:
        print('its away')
        return False

def is_night(): #calcula se esta visivel
    sunset_request = requests.get(f'https://api.sunrise-sunset.org/json?lat={my_lat}&lng={my_lgn}&formatted=0')
    sunset_request.raise_for_status() #catch error
    data = sunset_request.json()
    sunrise_hour = int(data['results']['sunrise'].split("T")[1].split(':')[0])
    sunset_hour = int(data['results']['sunset'].split("T")[1].split(':')[0])
    actual_hour = datetime.now().hour
    if sunset_hour <= actual_hour <= sunrise_hour:
        print('it´s dark')
        return True
    else:
        print('it´s daylight')
        return False

####################################################

if iss_tracker() and is_night(): #se estiver proximo e visivel
    print('its possible to see ISS in the sky')
    newConnection = smtplib.SMTP('smtp.gmail.com')
    newConnection.starttls()
    newConnection.login(os.getenv('EMAIL_SENDER'),os.getenv('EMAIL_PASSWORD'))
    newConnection.sendmail(
        from_addr=os.getenv('EMAIL_SENDER'),
        to_addrs='jpebecker@gmail.com',
        msg='Subject:ISS LOCATED\n\nThe ISS is above you in the sky.'
    )