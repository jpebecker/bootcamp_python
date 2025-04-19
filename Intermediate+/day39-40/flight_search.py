import os,requests,json
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"
class FlightManager:
    def __init__(self):
        self.search_url = ''
        self.params = {
            'client_id': os.getenv('flight_api_key'),
            'client_secret': os.getenv('flight_api_secretkey'),
        }
        self.token = self.get_new_token()

    def get_new_token(self):
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': os.getenv('flight_api_key'),
            'client_secret': os.getenv('flight_api_secretkey')
        }
        response = requests.post(url='https://test.api.amadeus.com/v1/security/oauth2/token',
                                 headers=header, data=body)
        # New bearer token(30min)
        #print(f"Your token is {response.json()['access_token']}")
        #print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"Authorization": f"Bearer {self.token}"}
        query = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "false",
            "currencyCode": "BRL",
            "max": "10",
        }
        response = requests.get(
            url=FLIGHT_ENDPOINT,
            headers=headers,
            params=query,
        )

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("Response body:", response.text)
            return None

        return response.json()