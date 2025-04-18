import pandas,os,smtplib,requests,json
from dotenv import load_dotenv
from datetime import datetime, timedelta
from email.mime.text import MIMEText
####################################################################
stockmarket_request_url = 'https://www.alphavantage.co/query'
news_request_url = 'https://newsapi.org/v2/everything'
load_dotenv()
stockData = pandas.read_csv('stock_entries.csv')
###################################################################
def calc_stock(search:json):  # CALCULO DAS AÇOES
    # data de hoje
    today = datetime.today()
    # data formatada de ontem
    yesterday = today - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    # print("Ontem:", yesterday_str)
    # data formatada de anteontem
    before_yesterday = today - timedelta(days=2)
    before_yesterday_str = before_yesterday.strftime('%Y-%m-%d')
    # print("Anteontem:", before_yesterday_str)

    # print(f'Dia: {yesterday_str} : {search['Time Series (Daily)'][yesterday_str]}')
    # print(f'Dia: {before_yesterday_str} : {search['Time Series (Daily)'][before_yesterday_str]}')

    yesterday_openvalue = float(search['Time Series (Daily)'][yesterday_str]['1. open'])
    beforeYday_openvalue = float(search['Time Series (Daily)'][before_yesterday_str]['1. open'])
    # print(yesterday_openvalue)
    # print(beforeYday_openvalue)

    changed_value = ((yesterday_openvalue - beforeYday_openvalue) / beforeYday_openvalue) * 100

    if abs(changed_value) >= 5:
        print(f"ALERTA: Houve uma variação de {changed_value:.2f}% nos últimos dois dias.")
        msg = MIMEText(call_news(selected_stock), _charset='utf-8')
        msg['Subject'] = f'ALERTA: Mercado de Ações de {selected_stock}'
        msg['From'] = os.getenv('EMAIL_SENDER')
        msg['To'] = 'jpebecker@gmail.com'
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:  # envia e-mail
            connection.starttls()
            connection.login(user=os.getenv('EMAIL_SENDER'), password=os.getenv('EMAIL_PASSWORD'))
            connection.sendmail(from_addr=os.getenv('EMAIL_SENDER'),
                                to_addrs='jpebecker@gmail.com',
                                msg=msg.as_string())

        print('relatório enviado por e-mail')

    else:
        print(f"ATUALIZAÇÃO: A variação foi de {changed_value:.2f}% nos últimos dois dias.")
#######################################
def call_news(stock):
    #CONSULTA A BASE DE NOTICIAS
    news_params = {
        'q': f"{stock} news",
        'pageSize': 5,
        'apiKey': os.getenv('NEWS_API_KEY')
    }
    news_request = requests.get(news_request_url,params=news_params)
    news_request.raise_for_status()
    news_data = news_request.json()
    #print(news_data['articles'])
    formatted_news = ''
    for news in news_data['articles']:
        formatted_news += (f'\n{stock} CURRENT NEWS:\n'
                         f'Manchete: {news['title']}\n\n'
                         f'Mais Detalhes: {news['description']}\n')
    return formatted_news
#######################################################################EXIBITION
print(stockData)
print('------------------------------------------------------')

try:
    entry = int(input('\nDigite o INDEX da ação que será analisada: '))
    selected_row = stockData.loc[entry]
except (ValueError, KeyError):
    print("Entrada inválida. Certifique-se de digitar um número válido.")
    exit()

selected_stock = stockData.loc[entry]['STOCK']
selected_stock_name = stockData.loc[entry]['COMPANY_NAME']

print('\nSTOCK :       COMPANY NAME')
print(f'{selected_stock} : {selected_stock_name}\n')
stockmarket_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol": selected_stock,
    "outputsize" : 'compact',
    "apikey" : os.getenv('STOCKMARKET_API_KEY'),
}
###################CONSULTA AO STOCKmarket
stockmarket_request = requests.get(stockmarket_request_url, params=stockmarket_params)
stockmarket_request.raise_for_status()
data = stockmarket_request.json()
calc_stock(search=data)
#########################################################