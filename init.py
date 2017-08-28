#!/usr/bin/env python
# -*- coding: utf-8 -*-
from version_checker import read_input
import sqlite3, bcrypt, getpass
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text, pass BLOB)''')
username = read_input("Моля, въведете потребителско име:")
password = getpass.getpass(prompt="Моля, въведете парола:")
password2 = getpass.getpass(prompt="Моля, повторете въведената парола:")
if(password != password2):
    exit("Паролите не съвпадат!")
hashed_pass =bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
print (username, hashed_pass)
c.execute("INSERT INTO users(username, pass) VALUES (?,?)", (username,hashed_pass))
conn.commit()
