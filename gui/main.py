from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder="./templates")

@app.route("/")
def root():
    return render_template('homepage.html')