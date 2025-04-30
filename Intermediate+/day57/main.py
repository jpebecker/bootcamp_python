import requests
from flask import Flask, render_template
from datetime import datetime
import requests
app = Flask(__name__)
y = datetime.today().year
data = requests.get('https://api.npoint.io/c790b4d5cab58020d391')
data.raise_for_status()
blogposts = data.json()

@app.route('/')
def home():
    return render_template("index.html",actual_year=y, blogdata=blogposts)

@app.route('/<postnumber>')
def blogpost(postnumber):
    return render_template("post.html",blogID=postnumber,actual_year=y,blogdata=blogposts[int(postnumber)-1])

if __name__ == "__main__":
    app.run(debug=True)
