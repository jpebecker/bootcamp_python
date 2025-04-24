import random
from flask import Flask
app = Flask(__name__)
def gen_random_number():
    return random.randint(0,9)

@app.route('/') #homepage
def initial_page():
    return '<h1 style="text-align: center">Adivinhe um número entre 0 e 9</h1>' \
            '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" style="display: block; margin: auto;">' \
            '<p style="text-align: center">Coloque a sua tentativa no final da URL' \
            '<p style="text-align: center">Exemplo: url/3'
num = gen_random_number()
@app.route('/<value>')
def calc_value(value):
    if int(value)>num:
        return '<h1 style="text-align: center">O valor é menor</h1>' \
               '<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDdhYjBzYmNwcnFwdzVveHFlYzJhNDhzNnhmMHU0bjl2YTFyYndwbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gKHGnB1ml0moQdjhEJ/giphy.gif" style="display: block; margin: auto;">' \
               '<p style="text-align: center">tente novamente'
    elif int(value)<num:
        return '<h1 style="text-align: center">O valor é maior</h1>' \
               '<img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExcjM3aTB3d2doaG01Zzl0NDRpMDQ3YzJ6djJlMTNjM2R3NXowN3pociZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/BBNYBoYa5VwtO/giphy.gif" style="display: block; margin: auto;">' \
               '<p style="text-align: center">tente novamente'
    elif int(value)==num:
        return '<h1 style="text-align: center">Parabéns! Você acertou</h1>' \
               '<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ2Z0OXh3OGIxZ2VtdHl5OWwxMzZmODZza2VtcW9peW9jdjh3bmYxYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT5LMHxhOfscxPfIfm/giphy.gif" style="display: block; margin: auto;">' \
               '<p style="text-align: center">Até a próxima'

if __name__ == '__main__':
    app.run(debug=True)