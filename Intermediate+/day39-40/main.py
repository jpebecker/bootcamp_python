from data_manager import DataManager
from flight_search import FlightManager
from flight_finder import find_cheapest_flight
from datetime import datetime,timedelta
import os,smtplib
from email.mime.text import MIMEText
#######################################################
origin_City = 'FLN'
sheet_data = DataManager()
Flight_Man = FlightManager()
cities_code = [item['code'] for item in sheet_data.formatted_data['prices']]

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
########################################################
for destination in sheet_data.formatted_data['prices']:
    print(f"\nGetting flights for {destination['city']}...")
    flights = Flight_Man.check_flights(
        origin_City,
        destination["code"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: R${cheapest_flight.price}")
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")
        sheet_data.update_data(row_number=f'{cities_code.index(destination['code'])}',lowest_price=cheapest_flight.price)

        message = f"Alerta de Preço baixo! Apenas R${cheapest_flight.price} para viajar\n"\
                  f"DE {cheapest_flight.origin_airport} PARA {cheapest_flight.destination_airport},\n"\
                  f"DO DIA {cheapest_flight.out_date} ATÉ {cheapest_flight.return_date}."
        msg = MIMEText(message, _charset='utf-8')
        msg['Subject'] = f'ALERTA: Preço de Viagens'
        msg['From'] = os.getenv('EMAIL_SENDER')
        msg['To'] = 'jpebecker@gmail.com'
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:  # envia e-mail
            connection.starttls()
            connection.login(user=os.getenv('EMAIL_SENDER'), password=os.getenv('EMAIL_PASSWORD'))
            connection.sendmail(from_addr=os.getenv('EMAIL_SENDER'),
                                to_addrs='jpebecker@gmail.com',
                                msg=msg.as_string())
        print('relatório enviado por e-mail')

