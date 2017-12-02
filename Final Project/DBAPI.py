import sqlite3

def connect(func):
    def func_wrapper(*args, **kwargs):
        conn = sqlite3.connect("myDB.db")
        return func(*args, **kwargs)
        conn.close()
    return func_wrapper

#TODO check and edit function
@connect
def createUsers(conn):
    try:
        conn.execute('''CREATE TABLE USERS
           (username text, hashresult text, salt text, role text)''')
        conn.commit()
    except(sqlite3.OperationalError):
        print('')

@connect
def createSites(conn):
    try:
        conn.execute('''CREATE TABLE SITES
           (siteid text, siteurl text)''')
        conn.commit()
    except(sqlite3.OperationalError):
        print('')

@connect
def createVoteReport(conn):
    try:
        conn.execute('''CREATE TABLE VOTEREPORT
           (username text, first text, second text, third text)''')
        conn.commit()
    except(sqlite3.OperationalError):
        print('')

#TODO check and edit function
@connect
def addUser(conn, username, hashresult, salt, role):
    c = conn.cursor()
    t = (username,)
    c.execute('SELECT * FROM USERS WHERE username=?', t)
    data = c.fetchone()
    if (data is None):
        params = (username, hashresult, salt, role)
        c.execute("INSERT INTO USERS VALUES (?, ?, ?, ?)", params)
        conn.commit()
        return True
    else:
        return False

@connect
def addSite(conn, siteid, siteurl):
    c = conn.cursor()
    t = (siteid,)
    c.execute('SELECT * FROM SITES WHERE siteid=?', t)
    data = c.fetchone()
    if (data is None):
        params = (siteid, siteurl)
        c.execute("INSERT INTO SITES VALUES (?, ?)", params)
        conn.commit()
        return True
    else:
        return False

@connect
def addVote(conn, username, first, second, third):
    c = conn.cursor()
    t = (username,)
    c.execute('SELECT * FROM VOTEREPORT WHERE username=?', t)
    data = c.fetchone()
    if (data is None):
        params = (username, first, second, third)
        c.execute("INSERT INTO VOTEREPORT VALUES (?, ?, ?, ?)", params)
        conn.commit()
        return True
    else:
        return False
