from flask import Flask, render_template
import sqlite3,os,requests

app = Flask(__name__, instance_relative_config=True)
#db path
db_path = os.path.join(app.instance_path, 'votes.db')
#api's urls
#cats apis
fact_c = 'https://meowfacts.herokuapp.com/' #meow facts
gif_c = 'https://cataas.com/cat/gif' #cataas
pic_c = 'htps://cataas.com/cat/cute' #cataas
#dogs apis
fact_d = 'https://dogapi.dog/api/v2/facts' #kinduff
pic_d = 'https://random.dog/woof.json'
#-------------------------------------------------------
#initialize db
def create_db():
    if not os.path.exists(db_path):
        os.makedirs(app.instance_path, exist_ok=True)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('CREATE TABLE votes (id INTEGER PRIMARY KEY, cats INTEGER DEFAULT 0, dogs INTEGER DEFAULT 0)')
        c.execute('INSERT INTO votes (cats, dogs) VALUES (0, 0)')
        conn.commit()
        conn.close()

#update votes
def add_vote(animal):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f'UPDATE votes SET {animal} = {animal} + 1 WHERE id = 1')
    conn.commit()
    c.execute('SELECT cats, dogs FROM votes WHERE id = 1')
    data = c.fetchone()
    conn.close()
    return data  # retorna os votos atualizados

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dog-person')
def dogs():
    #Getting api data
    dog_fact = requests.get(fact_d)
    dog_fact.raise_for_status()
    fact_value = dog_fact.json()['data'][0]['attributes']['body']

    dog_img = requests.get(pic_d)
    dog_img.raise_for_status()
    print(dog_img.status_code)
    dog_url = dog_img.json()['url']
    #------------
    cats_votes, dogs_votes = add_vote('dogs')
    return render_template('dogs.html', cats=cats_votes, dogs=dogs_votes,fact=fact_value,image=dog_url)

@app.route('/cat-person')
def cats():
    #Getting api data
    cat_fact = requests.get(fact_c)
    cat_fact.raise_for_status()
    fact_value = cat_fact.json()['data'][0]

    headers = {
        "Accept": "application/json",  # Isso normalmente é usado para APIs REST que retornam JSON
        "Content-Type": "application/json"  # Esse cabeçalho é irrelevante em GET sem corpo, mas aqui está como exemplo
    }
    gif_request = requests.get(gif_c, headers=headers)
    gif_request.raise_for_status()
    gif_url = gif_request.json()['url']

    #--------------
    cats_votes, dogs_votes = add_vote('cats')
    return render_template('cats.html', cats=cats_votes, dogs=dogs_votes,fact=fact_value,image=gif_url)

if __name__ == '__main__':
    create_db()
    app.run(debug=True)