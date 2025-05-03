from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, login_required, current_user, logout_user, LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
#LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

#Model de User para a DB
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

with app.app_context():
    db.create_all()

#Carregar user se tiver loggado
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

############################################## ROUTES
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.session.query(User).filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('secrets'))
        else:
            flash("Usuário ou senha incorretos.")

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html")


#Função para atribuir logged_in
@app.context_processor
def inject_user():
    return dict(logged_in=current_user.is_authenticated)


@app.route('/logout')
@login_required
def logout():
    logout_user()  #rota de logout do user
    return redirect(url_for('home'))


@app.route('/download', methods=['GET'])
@login_required
def download():
    file_name = 'cheat_sheet.pdf'
    directory = os.path.join(app.root_path, 'static', 'files')
    if os.path.exists(os.path.join(directory, file_name)):
        return send_from_directory(directory=directory, path=file_name)
    else:
        flash('File not found in server!')
        return redirect(url_for('secrets'))

if __name__ == "__main__":
    app.run(debug=True)