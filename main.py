import asyncio
import sqlite3
import threading
import time
import webview
from flask import Flask
from flask import render_template, request
from win11toast import toast

app = Flask(__name__, template_folder="./gui/templates", static_folder="./gui/static")
window = webview.create_window('Notifier App', app, width=1920, height=1080)

BASE_URL = 'http://127.0.0.1:35505'
LI = ['id', 'type', 'read', 'title', 'body', 'sender', 'image_url', 'timestamp']

from gmail import gmail
import json

import threading

MAIL = gmail.GMAIL()


def notification_toast_handler(id_, notif_type, notif_output: dict):
    if notif_type == "email":
        if notif_output['arguments'] == "http:Mark as Read":
            mark_email_as_read(id_)
        elif notif_output['arguments'] == "http:Open":
            mark_email_as_read(id_)
            window.evaluate_js(f"window.location.hash = 'view-email?id={id_}'")

    elif notif_type == "reminder":
        if notif_output['arguments'] == "http:Mark as Read":
            mark_reminder_as_read(id_)
        elif notif_output['arguments'] == "http:Open":
            mark_reminder_as_read(id_)
            window.evaluate_js(f"window.location.hash = 'view-reminder?id={id_}'")

    else:
        mark_notification_as_read(id_)


def mark_notification_as_read(notification_id):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("UPDATE notifications SET read=1 WHERE id=?", (notification_id,))
    db.commit()

    db.close()


def mark_reminder_as_read(notification_id):
    mark_notification_as_read(notification_id)


def mark_email_as_read(email_id):
    MAIL.mark_read(email_id)

    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute(f'UPDATE notifications SET read=1 WHERE id="{email_id}"')
    db.commit()

    db.close()


def send_reminder_notification(title, description, id_, image_url):
    buttons = [
        'Mark as Read',
        'Open'
    ]

    icon = {
        'src': image_url,
        'placement': 'appLogoOverride'
    }

    toast(
        f'Reminder: {title}', description, icon=icon, buttons=buttons,
        on_click=lambda notif_output: notification_toast_handler(id_, "reminder", notif_output),
        on_dismissed=lambda X: X
    )


def send_notification(title, description, id_, image_url):
    buttons = [
        'Mark as Read',
        'Open'
    ]

    icon = {  # TODO image_url can be none
        'src': image_url,
        'placement': 'appLogoOverride'
    }

    toast(
        f'{title}', description, buttons=buttons, icon=icon,
        on_click=lambda notif_output: notification_toast_handler('', '', notif_output),
        on_dismissed=lambda X: X
    )


def send_email_notification(id_, sender, title, description, timestamp, image_url):
    from win11toast import toast

    buttons = [
        'Mark as Read',
        'Open'
    ]

    icon = {

        'src': image_url,
        'placement': 'appLogoOverride'
    }

    toast(
        f'Reminder: {title}', description, icon=icon, buttons=buttons,
        on_click=lambda notif_output: notification_toast_handler(id_, "email", notif_output),
        on_dismissed=lambda X: X
    )


def setup_db():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute(
        "CREATE TABLE IF NOT EXISTS notifications (id TEXT, type TEXT, read INT, title TEXT, body TEXT, sender TEXT, image_url TEXT, timestamp INT)")
    db.commit()
    db.close()


setup_db()


@app.route("/")
def root():
    return render_template('homepage.html')


@app.route('/api/send-notification/', methods=['POST'])
def send_notification_():
    title = request.json['title']
    description = request.json['body']
    image_url = request.json['image_url']

    db = sqlite3.connect("database.db")
    c = db.cursor()

    with open('reminder.json', 'r') as f:
        count = json.load(f)['count']

    with open('reminder.json', 'w') as f:
        json.dump({'count': count + 1}, f)

    c.execute('INSERT INTO notifications values(?,?,?,?,?,?,?,?)',
              (str(count), 'api', 0, title, description, 0, image_url, int(time.time())))
    db.commit()

    db.close()

    send_notification(title, description, '', image_url)


@app.route('/api/reminders/')
def reminders():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute('SELECT id, title, body, timestamp FROM notifications WHERE type="reminder"')
    reminders_ = c.fetchall()
    reminders_ = sorted(reminders_, key=lambda x: x[-1], reverse=False)

    db.close()

    return {
        'http_code': 200,
        'data': [{'title': r[1], 'description': r[2], 'timestamp': r[-1], 'id': r[0]} for r in reminders_]
    }


@app.route('/api/reminders/<id_>')
def reminders_by_id(id_):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute(f'SELECT id, title, body, timestamp FROM notifications WHERE type="reminder" AND id="{id_}"')
    reminders_ = c.fetchone()

    db.close()

    print(reminders_)

    return {
        'http_code': 200,
        'data':
            {'title': reminders_[1], 'description': reminders_[2], 'timestamp': reminders_[-1], 'id': reminders_[0]}
    }


@app.route('/api/reminders/unread/')
def unread_reminders():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    req = ['id', 'type', 'title', 'body', 'sender', 'image_url', 'timestamp']

    c.execute(f"SELECT {', '.join(req)} FROM notifications WHERE read=0 AND timestamp >= {int(time.time())} AND type='reminder'")
    unread = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)

    db.close()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in unread]
    }

@app.route('/api/notifications/unread/')
def unread_notifications():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    req = ['id', 'type', 'title', 'body', 'sender', 'image_url', 'timestamp']

    c.execute(f'SELECT {", ".join(req)} FROM notifications WHERE read=0 AND timestamp <= {int(time.time())}')
    unread = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)

    db.close()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in unread]
    }


@app.route('/api/emails/')
def get_emails():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute('SELECT * FROM notifications WHERE type="email"')
    data = c.fetchall()
    db.close()

    return {
        "http_code": 200,
        "data": [{LI[i]: d[i] for i in range(len(d))} for d in data]
    }


@app.route('/api/emails/unread/')
def get_unread_emails():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute('SELECT * FROM notifications WHERE type="email" AND read=0')
    data = c.fetchall()
    db.close()

    return {
        "http_code": 200,
        "data": [{LI[i]: d[i] for i in range(len(d))} for d in data]
    }


@app.route("/api/notifications/")
def notifications():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    req = ['id', 'type', 'read', 'title', 'body', 'sender', 'image_url', 'timestamp']

    c.execute(f'SELECT {", ".join(req)} FROM notifications')
    notif = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)

    db.close()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in notif]
    }


@app.route("/api/reminders/delete/<id_>", methods=['DELETE'])
def delete_reminder(id_):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute(f"DELETE FROM notifications WHERE id={id_}")
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

    with open('reminder.json', 'r') as f:
        count = json.load(f)['count']

    with open('reminder.json', 'w') as f:
        json.dump({'count': count + 1}, f)

    c.execute("INSERT INTO notifications values (?,?,?,?,?,?,?,?)",
              (str(count + 1), 'reminder', 0, name, desc, 0, image_url, timestamp))
    db.commit()

    db.close()

    return {'http_code': 200}


def add_emails(emails):
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute('SELECT id FROM notifications WHERE type="email"')
    old = [i[0] for i in c.fetchall()]

    emails = [email for email in emails if email['id'] not in old]

    for mail in emails:
        c.execute("INSERT INTO notifications values (?,?,?,?,?,?,?,?)", 
                (mail['id'], 'email', 0, mail['subject'], mail['body'], mail['sender'],
                "https://img.icons8.com/?size=100&id=110231&format=png", mail['timestamp']))
        
        send_email_notification(title=mail['subject'], sender=mail['sender'], description=mail['body'], 
                                image_url=mail['image_url'], timestamp=mail['timestamp'])

    db.commit()
    db.close()


def check_for_notifications():
    def check():
        while True:

            emails = MAIL.unread_messages()
            if len(emails[0]):
                pass
            else:
                add_emails(emails[1])

            reminders = unread_notifications()['data']

            for r in reminders:
                if r['type'] != 'email':
                    send_reminder_notification(title=r['title'], description=r['body'], id_=r['id'],
                                               image_url=r['image_url'])

            time.sleep(15)

    thread = threading.Thread(target=check)
    thread.daemon = True
    thread.start()


check_for_notifications()

webview.start(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)


"""
rajs todo list

lightmode darkmode conversion
settings page
"""
