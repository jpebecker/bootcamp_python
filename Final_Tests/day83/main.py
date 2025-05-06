#A website to show off your skills and the things you've built.
import re,smtplib,os
from flask import Flask, render_template, request
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

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

app = Flask(__name__)
y = datetime.now().year

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=["GET", "POST"])
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


if __name__ == '__main__':
    app.run(debug=True)