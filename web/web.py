#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xxsubtype import spamdict

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask import render_template, flash, redirect, request
import pickle
import bcrypt
from ParamsForm import ParamsForm

app = Flask(__name__)
auth = HTTPBasicAuth()
users = {}
config = None
WTF_CSRF_ENABLED = True
app.secret_key = 'myverylongsecretkey'
def startApp(conf):
    global config
    config = conf
    app.run(host="0.0.0.0")
    app.debug=True



def getUser(username):
    global users
    with open('creds.txt', 'r') as f:
        for line in f:
            splitLine = line.split(':')
            user=splitLine[0]
            password=splitLine[1]
            filteredPass = password[2:-3]
            users[user] = filteredPass
    if username in users:
        return users.get(username)
    return None

@auth.verify_password
def verify_pw(username, plainpwd):
    hashedpwd = getUser(username)
    if hashedpwd is None or username is None or plainpwd is None:
        return False
    return bcrypt.hashpw(plainpwd, hashedpwd) == hashedpwd

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    global config
    form = ParamsForm()
    if request.method == 'GET':
        form.collectionInterval.data = int(config.getCollectionInterval())
        form.serverId.data = int(config.getServerId())
    if form.validate_on_submit():
        flash(u'Въведохте стойности интервал="%s", remember_me=%s' %
              (form.collectionInterval.data, str(form.serverId.data)))
        config.setCollectionInterval(int(form.collectionInterval.data))
        config.setServerId(int(form.serverId.data))
        with open('config.dat', 'wb') as file:
            pickle.dump(config.toJSON(), file)
        return redirect('/')
    return render_template('index.html',
                           title='Teams',
                           form=form,
                           config=config)

