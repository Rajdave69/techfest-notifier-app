from flask import Flask
from flask import render_template
import webview

app = Flask(__name__, template_folder="./templates")


@app.route("/")
def root():
    return render_template('homepage.html')


@app.route('/api/reminders/')
def reminders():
    # TODO make sure returned dict contains timestamp in decending order
    return {
        'http_code': 200,
        'data': [
            {'title': 'test', 'description': 'also eeetest', 'timestamp': '1717701680', 'id': '123'},
            {'title': 'test', 'description': 'also eeetest', 'timestamp': '1717703680', 'id': '123'},
            {'title': 'test', 'description': 'also eeetest', 'timestamp': '1717701680', 'id': '123'},


        ]

    }

@app.route('/api/notifications/unread/')
def unread_notifications():
    return {
        "http_code": 200,
        'data': [
            {'title': 'Title',
             'content': 'content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content concontent content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content contentcontent content content content content content content content content content content content content content content content content content content content content content content content  content content content tent content content content content content content content content ',
             'image': './static/placeholder_image.png', 'timestamp': '1717791543'},
            {'title': 'Title',
             'content': 'content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content concontent content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content contentcontent content content content content content content content content content content content content content content content content content content content content content content content  content content content tent content content content content content content content content ',
             'image': './static/placeholder_image.png', 'timestamp': '1717791543'},
            {'title': 'Title',
             'content': 'content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content concontent content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content contentcontent content content content content content content content content content content content content content content content content content content content content content content content  content content content tent content content content content content content content content ',
             'image': './static/placeholder_image.png', 'timestamp': '1717791543'}
        ]
    }

@app.route("/api/notifications/")
def notifications():
    return {
        "http_code": 200,
        'data': [
            {'title': 'Title',
             'content': 'content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content concontent content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content contentcontent content content content content content content content content content content content content content content content content content content content content content content content  content content content tent content content content content content content content content ',
             'image': './static/placeholder_image.png', 'timestamp': '1717791543'},
            {'title': 'Title',
             'content': 'content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content concontent content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content contentcontent content content content content content content content content content content content content content content content content content content content content content content content  content content content tent content content content content content content content content ',
             'image': './static/placeholder_image.png', 'timestamp': '1717791543'},
            {'title': 'Title',
             'content': 'content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content concontent content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content content contentcontent content content content content content content content content content content content content content content content content content content content content content content content  content content content tent content content content content content content content content ',
             'image': './static/placeholder_image.png', 'timestamp': '1717791543'}
        ]
    }

@app.route("/api/reminders/delete/{id}")
def delete_reminder():
    return {}

# webview.create_window('Notifier App', app, width=1920, height=1080)

# webview.start(debug=True)  # gui='mshtml' if it doesn't normally work
# webview.resize()
