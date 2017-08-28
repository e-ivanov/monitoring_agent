#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
import bcrypt
from flask_httpauth import HTTPBasicAuth
from flask import render_template, flash, redirect, request
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from version_checker import check_user_password
import sqlite3
import logging

conn = sqlite3.connect('users.db')
logger = logging.getLogger("web")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
app = Flask(__name__)
auth = HTTPBasicAuth()
users = {}
config = None
WTF_CSRF_ENABLED = True
app.secret_key = 'myverylongsecretkey'
logger = None
def start_app(conf, addr):
    global config, logger
    config = conf
    app.run(host=addr)
    app.logger = logger



def get_user(username):
    global conn
    if not username:
        return None
    try:
        c = conn.cursor()
        c.execute('SELECT pass FROM users WHERE username=?', (username,))
        result = c.fetchone()
        return result
    except Exception as e:
        print (e)

@auth.verify_password
def verify_pw(username, plainpwd):
    result_tuple = get_user(username)
    if result_tuple is None:
        return False
    hashedpwd = result_tuple[0]
    if hashedpwd is None or username is None or plainpwd is None:
        return False
    try:
        return check_user_password(plainpwd, hashedpwd)

    except Exception as e:
        print (e)

@app.errorhandler(500)
def internal_error(exception):
     app.logger.error(exception)
     return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    global config
    form = ParamsForm()
    if request.method == 'GET':
        form.collectionInterval.data = int(config.get("collection_interval", "interval"))
        form.serverId.data = int(config.get("server_id", "serverid"))
    if form.validate_on_submit():
        flash(u'Въведохте стойности интервал="%s", сървър=%s' %
              (form.collectionInterval.data, str(form.serverId.data)))
        config.set("collection_interval", "interval", form.collectionInterval.data)
        config.set("server_id", "serverid", form.serverId.data)
        config.save()
        return redirect('/')
    return render_template('index.html',
                           title='Teams',
                           form=form,
                           config=config)

class ParamsForm(Form):
    collectionInterval = StringField('collectionInterval', validators=[DataRequired()])
    serverId = StringField('serverId', validators=[DataRequired()])
