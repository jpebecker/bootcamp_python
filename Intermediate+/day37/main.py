import os,requests,json
from datetime import datetime

def create_pixela_user(): #to create a User in Pixela
    user_creation_url = 'https://pixe.la/v1/users'
    user_creation_params = {
        'token':os.getenv('PIXELA_API_KEY'),
        'username': os.getenv('PIXELA_USERNAME'),
        'agreeTermsOfService': 'yes',
        'notMinor': 'yes'
    }

    create_user_request = requests.post(user_creation_url,json=user_creation_params)
    print(create_user_request.text)

#create_pixela_user()
def create_new_graphic(): #to create a new graph
    create_graph_url = f'https://pixe.la/v1/users/{os.getenv('PIXELA_USERNAME')}/graphs'
    graph_params = {
        'id': 'gymtracker',
        'name': 'Gym Workout Attendance Graph',
        'unit': 'Days',
        'type': 'int',
        'color': 'momiji',
    }
    header = {
        'X-USER-TOKEN': os.getenv('PIXELA_API_KEY')
    }
    request_to_create_graph = requests.post(url=create_graph_url,json=graph_params,headers=header)
    print(request_to_create_graph.text)

#create_new_graphic()
def add_dot_to_graph(workout_type : str):
    post_to_graph_url = f'https://pixe.la/v1/users/{os.getenv('pixela_username')}/graphs/{'gymtracker'}'
    header = {
        'X-USER-TOKEN': os.getenv('PIXELA_API_KEY')
    }
    add_params={
        'date': datetime.today().strftime('%Y%m%d'), #required as string
        'quantity':'1', #required as string
        'optionalData': json.dumps({"Workout": f"{workout_type}"}),
    }
    add_to_graph_request = requests.post(url=post_to_graph_url,json=add_params,headers=header)
    print(add_to_graph_request.text)

def delete_dot(date:datetime):
    date = date.strftime('%Y%m%d')
    delete_url = f'https://pixe.la/v1/users/{os.getenv('pixela_username')}/graphs/gymtracker/{date}'
    header = {
        'X-USER-TOKEN': os.getenv('PIXELA_API_KEY')
    }
    request_to_delete_dot = requests.delete(url=delete_url,headers=header)
    print(request_to_delete_dot.text)

#delete_dot()

workouts = ['Chest', 'Back', 'Fight', 'Legs', 'Cardio']
while True:
    entry = input(f'Digite o tipo de Treino {workouts}:\n').strip().title()
    if entry in workouts:
        print(f'added to graph in {datetime.today().strftime('%Y%m%d')}')
        add_dot_to_graph(entry)
        break
    else:
        print('Erro de Entrada. Tente novamente.')