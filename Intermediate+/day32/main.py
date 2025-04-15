from dotenv import load_dotenv #carrega as credenciais pessoais como endereço e senha
import os,smtplib,pandas,random
from datetime import datetime
from email.mime.text import MIMEText #biblioteca do email para converter a mensagem com acentos
###########################################################
dict_of_people = pandas.read_csv("birthdays.csv").to_dict(orient="records")
load_dotenv()  # carrega as var do .env
email_sender = os.getenv("EMAIL_SENDER")
email_password = os.getenv("EMAIL_PASSWORD")
email_destination = ''
name = ''
for p in dict_of_people:
    if (datetime.today().month,datetime.today().day) == (p['month'],p['day']):
        email_destination = p['email']
        name = p['name']
#######################################################################
letters = ['letter_1','letter_2','letter_3']
with open(file=f'letters/{random.choice(letters)}.txt',mode='r',encoding='utf-8') as letter:
    msg_text = '\n'.join(letter.readlines())
    msg_text = msg_text.replace("NAME",name)
########################################################################
msg = MIMEText(msg_text, _charset='utf-8')
msg['Subject'] = 'Feliz aniversário'
msg['From'] = email_sender
msg['To'] = email_destination

with smtplib.SMTP('smtp.gmail.com', port=587) as connection: #envia e-mail
    connection.starttls()
    connection.login(user=email_sender, password=email_password)
    connection.sendmail(from_addr=email_sender,
                        to_addrs=email_destination,
                        msg=msg.as_string())
