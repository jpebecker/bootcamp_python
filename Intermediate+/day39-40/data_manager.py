import os,requests,json

class DataManager:
    def __init__(self):
        self.sheets_url = f'https://api.sheety.co/{os.getenv('SHEETY_ID')}/flightsApi/prices'
        self.sheets_header={
        "Authorization": f"Bearer {os.getenv('sheety_flight_api_key')}"
    }
        self.formatted_data = self.get_data()

    def get_data(self):
        newrequest = requests.get(url=self.sheets_url,headers=self.sheets_header)
        # salva os dados
        # with open('sheets.json', 'w', encoding='utf-8') as file:
        #     json.dump(newrequest.json(), file, ensure_ascii=False, indent=4)
        return newrequest.json()

    def update_data(self,row_number,lowest_price):
        body = {
            'price':{
                'lowestPrice':lowest_price
            }
        }
        self.sheets_header['Content-Type'] = 'application/json'
        newrequest = requests.put(url=f'{self.sheets_url}/{int(row_number)+2}', headers=self.sheets_header,json=body)
        print(newrequest.text)

