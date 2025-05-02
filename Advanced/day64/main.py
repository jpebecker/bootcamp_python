from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

#SQLite
db_path = os.path.join(instance_path, 'movies.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Classe Movie
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(1000), nullable=True)
    img_url = db.Column(db.String(500), nullable=False)

#Criando a tabela
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.ranking.asc()).all() #reordena os filmes por ordem de ranking
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        title = request.form["title"]
        year = request.form["year"]
        description = request.form["description"]
        rating = request.form["rating"]
        ranking = request.form["ranking"]
        review = request.form["review"]
        img_url = request.form["img_url"]

        new_movie = Movie(
            title=title,
            year=year,
            description=description,
            rating=rating,
            ranking=ranking,
            review=review,
            img_url=img_url
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add.html")

@app.route('/edit_movie/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):
    movie = Movie.query.get_or_404(id)

    if request.method == 'POST':
        movie.title = request.form['title']
        movie.year = request.form['year']
        movie.description = request.form['description']
        movie.rating = request.form['rating']
        movie.ranking = request.form['ranking']
        movie.review = request.form['review']
        movie.img_url = request.form['img_url']

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', movie=movie)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_movie(id):
    movie_to_delete = Movie.query.get(id)
    if movie_to_delete:
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)