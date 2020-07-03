import sqlite3
import configparser
from sqlite3 import Error

import datetime
import requests
import smtplib
import ssl

import User
import Watch

config = configparser.ConfigParser()
config.read("./settings.cfg")

# SQLite settings
db_file = config['TECHNICAL']['dbFile']

# server status settings
url = config['SERVER']['url']

# email settings
port = config['EMAIL']['port']
sender_email = config['EMAIL']['sender_email']
password = config['EMAIL']['password']


# --------

def main():
    _conn = establish_db_connection()

    online_players = query_online_players()

    print(online_players)

    users = query_users(_conn)

    for user in users:
        watched_players_online = []
        print(user)
        watches = query_watches(_conn, user.ID)
        for watch in watches:
            print(watch)
            if watch.Username in online_players:
                if watch.LastNotify is None or datetime.datetime.strptime(watch.LastNotify,
                                                                          '%Y-%m-%d %H:%M:%S.%f') < datetime.datetime.now() - datetime.timedelta(
                        hours=1):
                    watched_players_online.append(watch.Username)
                    update_watch_lastnotify(_conn, watch.ID)
        if len(watched_players_online) > 0:
            send_email(user.Email, generate_email(watched_players_online))
            print(f"{str(datetime.datetime.now())} - sent email to {user.Email}")

    _conn.close()


def establish_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def query_online_players():
    raw = requests.get(url)
    json = raw.json()
    if json['players']['online'] == 0:
        return []
    return json['players']['list']


def query_users(conn):
    users = []
    cur = conn.cursor()
    cur.execute("SELECT * from Users")

    rows = cur.fetchall()

    for row in rows:
        user = User.User(row[0], row[1], row[2], row[3], row[4])
        users.append(user)
    return users


def query_watches(conn, uid):
    watches = []
    cur = conn.cursor()
    cur.execute(f"SELECT * from Watches where UserID = {uid}")

    rows = cur.fetchall()

    for row in rows:
        watch = Watch.Watch(row[0], row[1], row[2], row[3])
        watches.append(watch)
    return watches


def update_watch_lastnotify(conn, watch_id):
    cur = conn.cursor()
    cur.execute(f"UPDATE Watches SET LastNotify = '{datetime.datetime.now()}' WHERE ID = {watch_id}")
    conn.commit()


def generate_email(username_list):
    message = f"Subject: Friends Online: {str(len(username_list))}\n\nThe following friends are currently online:\n\n"
    for name in username_list:
        message += f"\t{name}\n"
    return message


def send_email(recipient, message):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, message)


main()
