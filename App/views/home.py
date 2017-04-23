import hashlib
from codecs import encode
from tempfile import gettempdir

from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from flask_session import Session

from App.helpers import *
from App import app
from App import mysql

from App.views import admin


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if session.get('auth_lvl')      == 0:
        if request.method == 'POST':
            return admin.add(request.form.get('username'), request.form.get("approval"))
        else:
            db = mysql.connection.cursor()
            db.execute("SELECT * FROM tempusers ORDER BY fname")
            return render_template('index_a.html', rows=db.fetchall())


    elif session.get('auth_lvl')    == 1:
        return render_template('index_m.html')


    elif session.get('auth_lvl')    == 2:
        if request.method == 'POST':
            return None
        else:
            db = mysql.connection.cursor()
            if app.config['stage'] < 2:
                return render_template('failure.html', msg="This phase hasn't started yet")

            elif app.config['stage'] == 2:
                db.execute("SELECT * FROM candidates ORDER BY fname")
                return render_template('index_i.html', rows=db.fetchall())

            elif app.config['stage'] == 3:
                db.execute("SELECT * FROM selected ORDER BY fname")
                return render_template('index_i.html', rows=db.fetchall())

            else:
                return render_template('failure.html', msg="This phase has ended")


    else:
        db = mysql.connection.cursor()
        db.execute("SELECT * FROM candidates WHERE uid = {}".format(session['user_id']))
        return render_template('index.html', user=db.fetchone())

