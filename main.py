import asyncio
import sqlite3
import threading
import time
import webview
from flask import Flask
from flask import render_template, request

app = Flask(__name__, template_folder="./gui/templates", static_folder="./gui/static")
window = webview.create_window('Notifier App', app, width=1920, height=1080)

BASE_URL = 'http://127.0.0.1:35505'


#
#   GMAIL PART
#


from gmail import gmail

gmail = gmail.GMAIL

#
#   NOTIFICATIONS PART
#


def notification_toast_handler(notification_id, notif_output: dict):
    if notif_output['arguments'] == "http:Mark as Read":
        mark_notification_as_read(notification_id)
    elif notif_output['arguments'] == "http:Open":
        window.evaluate_js(f"window.location.hash = 'view-reminder?id={notification_id}'")


def email_toast_handler(email_id, notif_output: dict):
    if notif_output['arguments'] == "http:Mark as Read":
        mark_email_as_read(email_id)
    elif notif_output['arguments'] == "http:Open":
        window.evaluate_js(f"window.location.hash = 'view-email?id={email_id}'")


def mark_notification_as_read(notification_id):
    pass  # TODO RAYAN


def mark_email_as_read(email_id):
    pass  # TODO RAYAN


def send_reminder_notification(title, description, id_, image_url):
    from win11toast import toast

    buttons = [
        'Mark as Read',
        'Open'
    ]

    icon = {

        'src': 'https://unsplash.it/64?image=669',
        'placement': 'appLogoOverride'
    }

    toast(
        f'Reminder: {title}', description, icon=icon, buttons=buttons,
        on_click=lambda notif_output: notification_toast_handler(id_, notif_output),
        on_dismissed=lambda X: X
    )


def send_email_notification(title, description, id_, image_url):
    from win11toast import toast

    buttons = [
        'Mark as Read',
        'Open'
    ]

    icon = {

        'src': 'https://unsplash.it/64?image=669',
        'placement': 'appLogoOverride'
    }

    toast(
        f'Reminder: {title}', description, icon=icon, buttons=buttons,
        on_click=lambda notif_output: notification_toast_handler(id_, notif_output),
        on_dismissed=lambda X: X
    )


def setup_db():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, read INT, title TEXT, body TEXT, sender TEXT, image_url TEXT, timestamp INT)")
    db.commit()

    db.close()


setup_db()


@app.route("/")
def root():
    return render_template('homepage.html')

@app.route('/api/send-notification/', methods=['POST'])
def send_notification():
    title = request.json['title']
    description = request.json['body']

    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute('INSERT INTO notifications ') # TODO RAYAN ADD SQL
    # with timestamp 2 seconds later so it instantly notifies

@app.route('/api/reminders/')
def reminders():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute('SELECT id, title, body, timestamp FROM notifications WHERE type="reminder"')
    reminders_ = c.fetchall()
    reminders_ = sorted(reminders_, key=lambda x: x[-1], reverse=True)

    db.close()

    return {
        'http_code': 200,
        'data': [{'title': r[1], 'description': r[2], 'timestamp': r[-1], 'id': r[0]} for r in reminders_]
    }


@app.route('/api/notifications/unread/')
def unread_notifications():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    req = ['id', 'type', 'title', 'body', 'sender', 'image_url', 'timestamp']

    c.execute(f'SELECT {', '.join(req)} FROM notifications WHERE read=0 AND timestamp <= {int(time.time())}')
    unread = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)

    db.close()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in unread]
    }


@app.route("/api/notifications/")
def notifications():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    req = ['id', 'type', 'read', 'title', 'body', 'sender', 'image_url', 'timestamp']

    c.execute(f'SELECT {', '.join(req)} FROM notifications')
    notif = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)

    db.close()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in notif]
    }


@app.route("/api/reminders/delete/", methods=['POST'])
def delete_reminder():
    _id = request.json['id']
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute(f"DELETE FROM notifications WHERE id={_id}")
    db.commit()

    db.close()

    return {"http_code": 200}


@app.route("/api/reminders/create/", methods=['POST'])
def create_reminder():
    name = request.json["name"]
    timestamp = request.json["timestamp"]
    image_url = request.json["image_url"]
    desc = request.json['description']

    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("INSERT INTO notifications values (NULL,?,?,?,?,?,?,?)", (
        'reminder', 0, name, desc, 0, image_url, timestamp))
    db.commit()

    db.close()

    return {'http_code': 200}


# webview.resize()


def check_for_notifications():
    while True:
        # TODO RAYAN
        time.sleep(1)



notification_checker_thread = threading.Thread(target=check_for_notifications)
notification_checker_thread.start()

# send_notification_thread = threading.Thread(target=send_notification)
# send_notification_thread.start()

webview.start(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)


"""
rajs todo list

lightmode darkmode conversion
settings page
"""
