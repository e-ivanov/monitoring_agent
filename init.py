import sqlite3, sys, bcrypt
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text, pass BLOB)''')
username = sys.argv[1]
password = sys.argv[2]
hashed_pass =bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
print (username, hashed_pass)
c.execute("INSERT INTO users(username, pass) VALUES (?,?)", (username,hashed_pass))
conn.commit()
