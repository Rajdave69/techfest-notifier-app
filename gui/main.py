from flask import Flask
from flask import render_template, request
import webview
import sqlite3


app = Flask(__name__, template_folder="./templates")


def setup_db():
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, read INT, title TEXT, body TEXT, sender TEXT, image_url TEXT, timestamp INT)")
    db.commit()

    db.close()

setup_db()


@app.route("/")
def root():
    return render_template('homepage.html')


@app.route('/api/reminders/')
def reminders():
    
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute('SELECT id, title, body, timestamp FROM notifications WHERE type="reminders"')
    reminders = sorted(c.fetchall(), key=lambda x:x[-1], reverse=True)

    db.close()

    return {
        'http_code': 200,
        'data': [{'title':r[1], 'description':r[2], 'timestamp':r[-1], 'id':r[0]} for r in reminders]

    }

@app.route('/api/notifications/unread/')
def unread_notifications():

    db = sqlite3.connect("database.db")
    c = db.cursor()

    req = ['id', 'type', 'title', 'body', 'sender', 'image_url', 'timestamp']

    c.execute(f'SELECT {', '.join(req)} FROM notifications WHERE read=0')
    unread = sorted(c.fetchall(), key=lambda x:x[-1], reverse=True)
    
    db.close()

    return {
        "http_code": 200,
        'data': [{req[i]:u[i] for i in range(len(req))} for u in unread]
    }

@app.route("/api/notifications/")
def notifications():

    db = sqlite3.connect("database.db")
    c = db.cursor()

    req = ['id', 'type', 'read', 'title', 'body', 'sender', 'image_url', 'timestamp']

    c.execute(f'SELECT {', '.join(req)} FROM notifications')
    notif = sorted(c.fetchall(), key=lambda x:x[-1], reverse=True)
    
    db.close()

    return {
        "http_code": 200,
        'data': [{req[i]:u[i] for i in range(len(req))} for u in notif]
    }

@app.route("/api/reminders/delete/", methods=['POST'])
def delete_reminder():
    _id = request.form['id']
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute(f"DELETE FROM notifications WHERE id={_id}")
    db.commit()

    db.close()

    return {"http_code": 200}

@app.route("/api/reminders/create/", methods=['POST'])
def create_reminder():
    print(request)
    print(request.json)
    print(request.form.get('description'))
    print("hello")
    name = request.json["name"]
    timestamp = request.json["timestamp"]
    image_url = request.json["image_url"] 
    desc = request.json['description']
    print(name, timestamp, image_url, desc)

    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("INSERT INTO notifications values(NULL,?,?,?,?,?,?,?)", (
        'reminder', 0, name, desc, 0, image_url, timestamp))
    db.commit()

    db.close()

    return {'http_code':200}



webview.create_window('Notifier App', app, width=1920, height=1080)

webview.start(debug=True)  # gui='mshtml'notifications WHERE  if it doesn't normally work
# webview.resize()

# if __name__ == '__main__':
#     app.run(debug=True)


"""
rajs todo list

fix size of pagecontent
lightmode darkmode conversion
settings page
view email page
view notification page
url breadcrumb
"""
