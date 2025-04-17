import requests
parameters = {
    'amount':10,
    'category':28,
    'type':'boolean',
}
data_request = requests.get('https://opentdb.com/api.php',params=parameters)
data_request.raise_for_status()
question_data = data_request.json()['results']
