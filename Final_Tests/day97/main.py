from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os,stripe

# ----------- initial assigns -----------

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_API_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #doesnt track db modifications

#stripe initial config
stripe.api_key = os.getenv("STRIPE_API_KEY")
publishable_key = os.getenv("STRIPE_PUB_KEY")

db = SQLAlchemy(app) #db association with flask

# ------------------- db models --------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50)) #not used
    last_name = db.Column(db.String(100))  #not used
    zip_code = db.Column(db.String(20)) #not used
    email = db.Column(db.String(150), unique=True, nullable=False) #used
    password = db.Column(db.String(150), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

# ------------------- FLASK-LOGIN --------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------- CONTEXT for TEMPLATES(pages) --------------------
@app.context_processor
def inject_now(): #date for footer
    return {'now': datetime.now()}

@app.context_processor
def inject_user(): #verify user
    return dict(current_user=current_user)

# ------------------- routes --------------------
@app.route('/')
def home():
    services = Service.query.all() #gets all registered services (registration of services not implemented)
    return render_template('index.html', services=services)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout(): #stripe pre-implementation
    if request.method == 'POST':
        try:
            service_id = request.form.get('service_id') #get the service selected
            service = Service.query.get(service_id)

            if service:
                intent = stripe.PaymentIntent.create(
                    amount=int(service.price * 100),  #cents prices
                    currency='brl', #currency
                    metadata={'service_id': str(service.id)}
                )
                return render_template('checkout.html',
                                       client_secret=intent.client_secret, #credencial
                                       publishable_key=publishable_key,
                                       service=service)
            else:
                flash('Serviço não encontrado!')
                return redirect(url_for('home'))
        except Exception as exc:
            flash(f'Ocorreu um erro: {str(exc)}')
            return redirect(url_for('home'))
    else:
        flash("Você deve escolher um serviço primeiro.")
        return redirect(url_for('home'))

@app.route('/service/<int:service_id>')
def view_service(service_id):
    service = Service.query.get_or_404(service_id)
    return render_template('services.html', service=service)

# ------------------- auth routes --------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas')
    return render_template('authenticate.html', action='login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        if User.query.filter_by(email=email).first():
            flash('Usuário já existe')
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
    return render_template('authenticate.html', action='register')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session(): #stripe implementation
    try:
        service_id = request.form.get('service_id')
        service = Service.query.get(service_id)

        if not service:
            flash('Serviço não encontrado.')
            return redirect(url_for('home'))

        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email, #show the customer email
            submit_type='pay',
            billing_address_collection='required', #needs billing adress
            shipping_address_collection={
                'allowed_countries': ['BR'],  # just for brazil
            },
            line_items=[{#item description on the stripe page
                'price_data': {
                    'currency': 'brl',
                    'product_data': {
                        'name': service.name,
                        'description': service.description,
                    },
                    'unit_amount': int(service.price * 100),  #this convert the price to cents (stripe requirement)
                },
                'quantity': 1,
            }],
            mode='payment', #i should update this if service is month subscription or one payment
            success_url=url_for('checkout_success', _external=True),
            cancel_url=url_for('checkout_cancel', _external=True),
        )

        return redirect(checkout_session.url, code=303)

    except Exception as e:
        flash(f"Ocorreu um erro: {str(e)}")
        return redirect(url_for('home'))

@app.route('/checkout-success')#if payment is sucessfull
def checkout_success():
    return render_template('success.html')

@app.route('/checkout-cancel')#if payment was interrupted
def checkout_cancel():
    return render_template('cancel.html')
# ------------------- main loop --------------------
if __name__ == '__main__': #runs everything
    with app.app_context():
        db.create_all()
    app.run(debug=True)