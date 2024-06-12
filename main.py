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
lock = threading.Lock()

db = sqlite3.connect("database.db", check_same_thread=False, timeout=20)
c = db.cursor()


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
    
    try:
        lock.acquire(True)
        c.execute("UPDATE notifications SET read=1 WHERE id=?", (notification_id,))
        db.commit()
    finally:
        lock.release()


def mark_reminder_as_read(notification_id):
    mark_notification_as_read(notification_id)


def mark_email_as_read(email_id):
    MAIL.mark_read(email_id)

    try:
        lock.acquire(True)
        c.execute(f'UPDATE notifications SET read=1 WHERE id="{email_id}"')
        db.commit()
    finally:
        lock.release()


def send_reminder_notification(title, body, id_, image_url):
    buttons = [
        'Mark as Read',
        'Open'
    ]

    icon = {
        'src': image_url,
        'placement': 'appLogoOverride'
    }

    toast(
        f'Reminder: {title}', body, icon=icon, buttons=buttons,
        on_click=lambda notif_output: notification_toast_handler(id_, "reminder", notif_output),
        on_dismissed=lambda X: X
    )


def send_notification(title, body, id_, image_url):
    buttons = [
        'Mark as Read',
        'Open'
    ]

    icon = {  # TODO image_url can be none
        'src': image_url,
        'placement': 'appLogoOverride'
    }

    toast(
        f'{title}', body, buttons=buttons, icon=icon,
        on_click=lambda notif_output: notification_toast_handler('', '', notif_output),
        on_dismissed=lambda X: X
    )


def send_email_notification(id_, sender, title, body, timestamp):
    print(sender)

    buttons = [
        'Mark as Read',
        'Open'
    ]

    toast(
        f'Email: {title}', body, buttons=buttons,
        on_click=lambda notif_output: notification_toast_handler(id_, "email", notif_output),
        on_dismissed=lambda X: X
    )


def setup_db():
    c.execute(
        "CREATE TABLE IF NOT EXISTS notifications (id TEXT, type TEXT, read INT, title TEXT, body TEXT, sender TEXT, image_url TEXT, timestamp INT)")
    db.commit()


setup_db()


@app.route("/")
def root():
    return render_template('homepage.html')


@app.route('/api/send-notification/', methods=['POST'])
def send_notification_():
    title = request.json['title']
    body = request.json['body']
    image_url = request.json['image_url']

    with open('reminder.json', 'r') as f:
        count = json.load(f)['count']

    with open('reminder.json', 'w') as f:
        json.dump({'count': count + 1}, f)

    try:
        lock.acquire(True)    
        c.execute('INSERT INTO notifications values(?,?,?,?,?,?,?,?)',
                (str(count), 'api', 0, title, body, 0, image_url, int(time.time())))
        db.commit()
    finally:
        lock.release()

    db.close()

    send_notification(title, body, '', image_url)


@app.route('/api/reminders/')
def reminders():

    try:
        lock.acquire(True)
        c.execute('SELECT id, title, body, timestamp FROM notifications WHERE type="reminder"')
        reminders_ = c.fetchall()
        reminders_ = sorted(reminders_, key=lambda x: x[-1], reverse=False)
    finally:
        lock.release()

    return {
        'http_code': 200,
        'data': [{'title': r[1], 'body': r[2], 'timestamp': r[-1], 'id': r[0]} for r in reminders_]
    }


@app.route('/api/reminders/<id_>')
def reminders_by_id(id_):

    try:
        lock.acquire(True)
        c.execute(f'SELECT id, title, body, timestamp FROM notifications WHERE type="reminder" AND id="{id_}"')
        reminders_ = c.fetchone()
    finally:
        lock.release()

    return {
        'http_code': 200,
        'data':
            {'title': reminders_[1], 'body': reminders_[2], 'timestamp': reminders_[-1], 'id': reminders_[0]}
    }


@app.route('/api/reminders/unread/')
def unread_reminders():
    req = ['id', 'type', 'title', 'body', 'sender', 'image_url', 'timestamp']

    try:
        lock.acquire(True)
        c.execute(f"SELECT {', '.join(req)} FROM notifications WHERE read=0 AND timestamp <= {int(time.time())} AND type='reminder'")
        unread = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)
    finally:
        lock.release()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in unread]
    }


@app.route('/api/notifications/unread/')
def unread_notifications():
    req = ['id', 'type', 'title', 'body', 'sender', 'image_url', 'timestamp']

    try:
        lock.acquire(True)
        c.execute(f'SELECT {", ".join(req)} FROM notifications WHERE read=0 AND timestamp <= {int(time.time())}')
        unread = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)
    finally:
        lock.release()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in unread]
    }


@app.route('/api/emails/')
def get_emails():

    try:
        lock.acquire(True)
        c.execute('SELECT * FROM notifications WHERE type="email"')
        data = c.fetchall()
    finally:
        lock.release()

    return {
        "http_code": 200,
        "data": [{LI[i]: d[i] for i in range(len(d))} for d in data]
    }


@app.route('/api/emails/unread/')
def get_unread_emails():

    try:
        lock.acquire(True)
        c.execute('SELECT * FROM notifications WHERE type="email" AND read=0')
        data = c.fetchall()
    finally:
        lock.release()

    return {
        "http_code": 200,
        "data": [{LI[i]: d[i] for i in range(len(d))} for d in data]
    }


@app.route("/api/notifications/")
def notifications():
    req = ['id', 'type', 'read', 'title', 'body', 'sender', 'image_url', 'timestamp']

    try:
        lock.acquire(True)
        c.execute(f'SELECT {", ".join(req)} FROM notifications')
        notif = sorted(c.fetchall(), key=lambda x: x[-1], reverse=True)
    finally:
        lock.release()

    return {
        "http_code": 200,
        'data': [{req[i]: u[i] for i in range(len(req))} for u in notif]
    }


@app.route("/api/reminders/delete/<id_>", methods=['DELETE'])
def delete_reminder(id_):

    try:
        lock.acquire(True)
        c.execute(f"DELETE FROM notifications WHERE id={id_}")
        db.commit()
    finally:
        lock.release()

    return {"http_code": 200}


@app.route("/api/reminders/create/", methods=['POST'])
def create_reminder():
    name = request.json["name"]
    timestamp = request.json["timestamp"]
    image_url = request.json["image_url"]
    desc = request.json['body']

    if not image_url: image_url = "https://img.icons8.com/?size=100&id=110472&format=png"

    with open('reminder.json', 'r') as f:
        count = json.load(f)['count']

    with open('reminder.json', 'w') as f:
        json.dump({'count': count + 1}, f)

    try:
        lock.acquire(True)
        c.execute("INSERT INTO notifications values (?,?,?,?,?,?,?,?)",
                (str(count + 1), 'reminder', 0, name, desc, 0, image_url, timestamp))
        db.commit()
    finally:
        lock.release()

    return {'http_code': 200}


def add_emails(emails):
    try:
        lock.acquire(True)
        c.execute('SELECT id FROM notifications WHERE type="email"')
        old = [i[0] for i in c.fetchall()]
    finally:
        lock.release()

    emails = [email for email in emails if email['id'] not in old]

    try:
        lock.acquire(True)
        for mail in emails:
            c.execute("INSERT INTO notifications values (?,?,?,?,?,?,?,?)", 
                    (mail['id'], 'email', 0, mail['subject'], mail['body'], mail['sender'],
                    "https://img.icons8.com/?size=100&id=110231&format=png", mail['timestamp']))
            
            send_email_notification(title=mail['subject'], sender=mail['sender'], 
                                    body=mail['body'], id_=mail['id'], timestamp=mail['timestamp'])

        db.commit()
    finally:
        lock.release()

def check_for_notifications():
    def check():
        while True:

            emails = MAIL.unread_messages()
            print(emails, '\n' * 5)

            if not emails:
                pass
            else:
                add_emails(emails[1])

            reminders = unread_notifications()['data']

            for r in reminders:
                if r['type'] != 'email':
                    send_reminder_notification(title=r['title'], body=r['body'], id_=r['id'],
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
