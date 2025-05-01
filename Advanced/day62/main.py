from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

class CafeForm(FlaskForm):
    cafe = StringField('Store name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[DataRequired(), URL()])
    open_time = TimeField('Open Time', format='%H:%M', validators=[DataRequired()])
    close_time = TimeField('Close Time', format='%H:%M', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=[(str(i), '☕️' * i) for i in range(6)],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Speed Rating',
                              choices=[(str(i), '🚀' * i) for i in range(6)],
                              validators=[DataRequired()])
    power_rating = SelectField('Wifi Power Rating',
                               choices=[(str(i), '💪' * i) for i in range(6)],
                               validators=[DataRequired()])
    submit = SubmitField('Update Database')

@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, lineterminator='\n')
            writer.writerow([
                form.cafe.data,
                form.location.data,
                form.open_time.data.strftime('%H:%M'),
                form.close_time.data.strftime('%H:%M'),
                form.coffee_rating.data,
                form.wifi_rating.data,
                form.power_rating.data
            ])
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        rows = list(reader)
    header = rows[0]
    data = rows[1:]
    def to_emoji(value, emoji_char):
        try:
            return emoji_char * int(value)
        except ValueError:
            return value

    transformed = []
    for row in data:
        cafe, loc, open_t, close_t, coffee, wifi, power = row
        transformed.append([
            cafe,
            loc,
            open_t,
            close_t,
            to_emoji(coffee, '☕️'),
            to_emoji(wifi, '🚀'),
            to_emoji(power, '💪')
        ])
    return render_template('cafes.html', cafes=transformed)

if __name__ == '__main__':
    app.run(debug=True)
