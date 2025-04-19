import os,requests,json,asyncio
from googletrans import Translator
from datetime import datetime
###########################################3
translator = Translator()
APP_HEADER = {
    'x-app-id': os.getenv('NUTRITIONIX_ID'),
    'x-app-key': os.getenv('NUTRITIONIX_API_KEY'),
}
search_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
sheets_url = f'https://api.sheety.co/{os.getenv('SHEETY_ID')}/refeicoesApi/mainPage'
sheets_header={
    "Authorization": f"Bearer {os.getenv('sheety_api_key')}"
}
#############################################
def calc_results(results:json):
    foods_eaten = [f"{item['serving_qty']}x {item['food_name']}" for item in results['foods']]
    calories = sum(item['nf_calories'] for item in results['foods'])
    newresults = {
        'calories' : round(calories,2),
        'foods' : ' / '.join(foods_eaten),
    }
    return newresults
async def main():
    entry = input('Digite sua refeição:\n')
    #Traduz do ptbr para en
    translated = await translator.translate(text=entry, src="auto", dest="en")
    translated_text = translated.text
    #print('Traduzido:', translated_text)

    #chama api nutricional
    food_params = {'query': translated_text}
    response = requests.post(url=search_url, json=food_params, headers=APP_HEADER)
    result = calc_results(response.json())

    formatted_results = {
        "mainPage": {
            "date": f'{datetime.today().strftime('%d/%m/%Y')}',
            "hour": f'{datetime.today().now().strftime("%H:%M:%S")}',
            "caloriesEaten" : f"{result['calories']}",
            "foodEaten" : f"{result['foods']}"
  }
}
    sheets_request = requests.post(url=sheets_url,json=formatted_results,headers=sheets_header)

    #salva os dados nutricionais
    # with open('foods.json', 'w', encoding='utf-8') as file:
    #     json.dump(result, file, ensure_ascii=False, indent=4)

asyncio.run(main())
print('dados importados para a Planilha no Google Sheets')