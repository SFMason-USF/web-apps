import sqlite3

def connect(func):
    def func_wrapper(*args, **kwargs):
        conn = sqlite3.connect("myDB.db")
        return func(*args, **kwargs)
        conn.close()
    return func_wrapper

#TODO check and edit function
@connect
def createTable(conn):
    try:
        conn.execute('''CREATE TABLE USERS
           (id text, password text, role boolean)''')
        conn.commit()
        # print('Table constructed')
    except(sqlite3.OperationalError):
        # print('ERROR: Table Was not constructed')
        print('    Table already exists.')

#TODO check and edit function
@connect
def getTable(conn):
    c = conn.execute("SELECT id, add_score, sub_score, multi_score, div_score from USERS")
    data = c.execute('SELECT * FROM USERS ORDER BY id')
    return data

#TODO check and edit function
# @connect
# def printTable(conn):
#     c = conn.execute("SELECT id, password, add_score, sub_score, multi_score, div_score, tscore from USERS")
#     print("|Username       |Password       |   ADD|   SUB| MULTI|   DIV|   TOTAL|")
#     print("|---------------+---------------+------+------+------+------+--------|")
#     for row in c.execute('SELECT * FROM USERS ORDER BY id'):
#         print('|{0:15}|{1:15}|{2:6}|{2:6}|{2:6}|{2:6}|{2:8}|'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
#     print ("")

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

#TODO check and edit function
@connect
def verifyUser(conn, user, password):
    t = (user,)
    c = conn.cursor()
    c.execute('SELECT * FROM USERS WHERE ID=?', t)
    data = c.fetchone()
    return ((data is not None) and (data[1] == password))

#TODO check and edit function
@connect
def updateUser(conn, user, USERS):
    c = conn.cursor()
    arg = USERS + (sum(USERS), user)
    print(arg)
    c.execute('UPDATE USERS SET add_score=?, sub_score=?, multi_score=?, div_score=?, tscore=? WHERE id=?',arg)
    print('Score updated for user:"{0}"'.format(arg[5]))
    conn.commit()

#TODO check and edit function
@connect
def getScore(conn,user):
    t = (user,)
    c = conn.cursor()
    c.execute('SELECT * FROM USERS WHERE ID=?', t)
    data = c.fetchone()
    return data[2:6]
