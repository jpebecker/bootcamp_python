from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os,smtplib,re
from email.mime.text import MIMEText
##################################################init
app = Flask(__name__)
app.secret_key = 'goanaofnoalnfoeamlkvalve'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
y = datetime.now().year
db = SQLAlchemy(app)
###################################################contact functions
def send_email(message):
    email = MIMEText(message, _charset='utf-8')
    email['Subject'] = f'Nova Mensagem do site To Do It'
    email['From'] = os.getenv('EMAIL_SENDER')
    email['To'] = 'jpebecker@gmail.com'
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:  # envia e-mail
        connection.starttls()
        connection.login(user=os.getenv('EMAIL_SENDER'), password=os.getenv('EMAIL_PASSWORD'))
        connection.sendmail(from_addr=os.getenv('EMAIL_SENDER'),
                            to_addrs='jpebecker@gmail.com',
                            msg=email.as_string())
        print('e-mail enviado')

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)
##############################################################
#user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email=db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

#task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    due_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('tasks', lazy=True))

#initial page info page
@app.route('/')
def home():
    return render_template('index.html')


#registration page
@app.route('/register-user', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('register'))
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('email already exists')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')


#login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # busca o usuário pelo e-mail
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # aqui você recupera o username do objeto user
            username = user.username

            # salva na sessão
            session['user_id'] = user.id
            session['username'] = username

            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

#logout function goes to homepage
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('home'))


#######################################contact route
@app.route("/contact-me",methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        msg = f'Enviado por: {name}\n Contato: {email}\n\n {request.form["message"]}'

        if not is_valid_email(email):
            return render_template("contact_fail.html", username=name, actual_year=y)

        send_email(message=msg)
        return render_template("contact_sucess.html", username=name, actual_year=y)

    return render_template("contact.html",actual_year = y)

#################################################TASKS ROUTES
#show taks
@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        flash('Você precisa estar logado para ver as tarefas.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_tasks = Task.query.filter_by(user_id=user_id).all()

    return render_template('tasks.html', tasks=user_tasks)

#add tasks
@app.route('/add-task', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        flash('Você precisa estar logado para adicionar tarefas.')
        return redirect(url_for('login'))

    task_name = request.form['task_name']
    task_date = request.form['due_date']
    due_date = datetime.strptime(task_date, '%Y-%m-%d') if task_date else None
    new_task = Task(name=task_name, user_id=session['user_id'], status='Pending', due_date=due_date)

    db.session.add(new_task)
    db.session.commit()

    flash('Tarefa adicionada com sucesso!')
    return redirect(url_for('tasks'))

#edit tasks
@app.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'user_id' not in session:
        flash('Você precisa estar logado para editar tarefas.')
        return redirect(url_for('login'))

    task = Task.query.get(task_id)
    if task.user_id != session['user_id']:
        flash('Você não tem permissão para editar esta tarefa.')
        return redirect(url_for('tasks'))

    if request.method == 'POST':
        task.name = request.form['task_name']
        task.status = request.form['status']
        task_date = request.form['due_date']
        task.due_date = datetime.strptime(task_date, '%Y-%m-%d') if task_date else None

        db.session.commit()
        flash('Tarefa atualizada com sucesso!')
        return redirect(url_for('tasks'))

    return render_template('edit_task.html', task=task)

#exclude tasks
@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    if 'user_id' not in session:
        flash('Você precisa estar logado para excluir tarefas.')
        return redirect(url_for('login'))

    task = Task.query.get(task_id)
    if task.user_id != session['user_id']:
        flash('Você não tem permissão para excluir esta tarefa.')
        return redirect(url_for('tasks'))

    db.session.delete(task)
    db.session.commit()

    flash('Tarefa excluída com sucesso!')
    return redirect(url_for('tasks'))

#context processor might be used
@app.context_processor
def inject_logged():
    return dict(logged=lambda: 'email' in session)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #create the db
    app.run(debug=True)