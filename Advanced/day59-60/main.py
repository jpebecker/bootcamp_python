import requests,re,smtplib,os
from flask import Flask, render_template, request
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

here = os.path.dirname(__file__)  
env_path = os.path.abspath(os.path.join(here, '..', '..', 'env_files', '.env'))
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
y = datetime.today().year
data = requests.get('https://api.npoint.io/c790b4d5cab58020d391')
data.raise_for_status()
blogposts = data.json()

def send_email(message):
    email = MIMEText(message, _charset='utf-8')
    email['Subject'] = f'Nova Mensagem do BLOG'
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

@app.route('/favicon.ico')#correcao de erro
def favicon():
    return '', 204

@app.route('/')
def home():
    return render_template("index.html",actual_year=y, blogdata=blogposts)

@app.route('/<postnumber>')
def blogpost(postnumber):
    return render_template("post.html",blogID=postnumber,actual_year=y,blogdata=blogposts[int(postnumber)-1])

@app.route('/about-me')
def aboutMe():
    return render_template("about.html",actual_year=y)

@app.route('/contact-me', methods=["GET", "POST"])
def contactMe():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        msg = f'Enviado por: {name}\n Contato: {email}\n\n {request.form["message"]}'

        if not is_valid_email(email):
            return render_template("contact_fail.html", username=name, actual_year=y)
        
        send_email(message=msg)
        return render_template("contact_sucess.html", username=name, actual_year=y)
    
    return render_template("contact.html", actual_year=y)

if __name__ == "__main__":
    app.run(debug=True)