from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)
# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///games.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Game(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)
    studio: Mapped[str] = mapped_column(String(100), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

# Create table schema.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    # READ ALL RECORDS
    result = db.session.execute(db.select(Game).order_by(Game.rating.desc())) #ordena por rating
    all_games = result.scalars().all()
    return render_template("index.html", games=all_games)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        #CREATE a RECORD
        new_game = Game(
            title=request.form["title"],
            studio=request.form["studio"],
            rating=request.form["rating"]
        )
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD
        game_id = request.form["id"]
        game_to_update = db.get_or_404(Game, game_id)
        game_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    game_id = request.args.get('id')
    game_selected = db.get_or_404(Game, game_id)
    return render_template("edit_rating.html", game=game_selected)


@app.route("/delete")
def delete():
    game_id = request.args.get('id')

    # DELETE A RECORD BY ID
    game_to_delete = db.get_or_404(Game, game_id)
    db.session.delete(game_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
