from flask import Flask
from flask import render_template
import webview

app = Flask(__name__, template_folder="./templates")


@app.route("/")
def root():
    return render_template('homepage.html')


@app.route('/potato')
def potato():
    return render_template()


# webview.create_window('Notifier App', app, width=1920, height=1080)

# webview.start(debug=True)  # gui='mshtml' if it doesn't normally work
# webview.resize()
