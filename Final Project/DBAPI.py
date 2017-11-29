import sqlite3

def connect(func):
    def func_wrapper(*args, **kwargs):
        conn = sqlite3.connect("myDB.db")
        return func(conn, *args, **kwargs)
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
@connect
def printTable(conn):
    c = conn.execute("SELECT id, password, add_score, sub_score, multi_score, div_score, tscore from USERS")
    print("|Username       |Password       |   ADD|   SUB| MULTI|   DIV|   TOTAL|")
    print("|---------------+---------------+------+------+------+------+--------|")
    for row in c.execute('SELECT * FROM USERS ORDER BY id'):
        print('|{0:15}|{1:15}|{2:6}|{2:6}|{2:6}|{2:6}|{2:8}|'.format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
    print ("")

#TODO check and edit function
@connect
def addUser(conn, userName, password):
    c = conn.cursor()
    t = (userName,)
    c.execute('SELECT * FROM USERS WHERE ID=?', t)
    data = c.fetchone()
    if (data is None):
        params = (userName, password,0,0,0,0,0)
        c.execute("INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?)", params)
        return True
        conn.commit()
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



# TODO check all this shit
# @connect
# def changePass(conn, user, password):
#     c = conn.cursor()
#     arg = (password,) + (user,)
#     c.execute('UPDATE USERS SET password=? WHERE id=?',arg)
#     print('Password Changed for user:"{0}"'.format(arg[1]))
#     conn.commit()

# @connect
# def loginHelper(conn, userName, password):
#     c = conn.cursor()
#     t = (userName,)
#     c.execute('SELECT * FROM USERS WHERE ID=?', t)
#     data = c.fetchone()
#     if (data is None):
#         params = (userName, password,0,0,0,0,0)
#         c.execute("INSERT INTO USERS VALUES (?, ?, ?, ?, ?, ?, ?)", params)
#         print('New user created:"{0}"'.format(params[0]))
#         conn.commit()
#         return 1
#     else:
#         return (data[1] == password)

# @connect
# def deleteUser(conn, user):
#     c = conn.cursor()
#     t = (user,)
#     c.execute("DELETE FROM USERS WHERE id=?",t)
#     print('Deleted user:"{0}"'.format(user))
#     conn.commit()


# def incAdd(user,val):
#     sc = getScore(user)
#     add = sc[0]+val
#     sc = (add,sc[1],sc[2],sc[3])
#     updateUser(user,sc)
    
# def incSub(user,val):
#     sc = getScore(user)
#     sub = sc[1]+val
#     sc = (sc[0],sub,sc[2],sc[3])
#     updateUser(user,sc)
    
# def incMulti(user,val):
#     sc = getScore(user)
#     multi = sc[2]+val
#     sc = (sc[0],sc[1],multi,sc[3])
#     updateUser(user,sc)
    
# def incDiv(user,val):
#     sc = getScore(user)
#     div = sc[3]+val
#     sc = (sc[0],sc[1],sc[2],div)
#     updateUser(user,sc)

# def setAdd(user,val):
#     sc = getScore(user)
#     sc = (val,sc[1],sc[2],sc[3])
#     updateUser(user,sc)
    
# def setSub(user,val):
#     sc = getScore(user)
#     sc = (sc[0],val,sc[2],sc[3])
#     updateUser(user,sc)
    
# def setMulti(user,val):
#     sc = getScore(user)
#     sc = (sc[0],sc[1],val,sc[3])
#     updateUser(user,sc)
    
# def setDiv(user,val):
#     sc = getScore(user)
#     sc = (sc[0],sc[1],sc[2],val)
#     updateUser(user,sc)

# def getAdd(user):
#     sc = getScore(user)
#     return sc[0]

# def getSub(user):
#     sc = getScore(user)
#     return sc[1]

# def getMulti(user):
#     sc = getScore(user)
#     return sc[2]

# def getDiv(user):
#     sc = getScore(user)
#     return sc[3]
    
# @connect
# def leaderBoard(conn,num):
#     c = conn.cursor()
#     c.execute("SELECT * FROM USERS ORDER BY tscore DESC LIMIT ?",(num,))
#     data = c.fetchall()
#     rdata = []
#     for row in data:
#         rdata.append((row[0],) + row[2:6])
#     return rdata


# #******************************************************************************
# # Application Main Routine (will not run when imported)
# #******************************************************************************
# def Main():
#     while(1):
#         print("")
#         print("=======================================================")
#         print("                    DBAPI.PY Utills                    ")
#         print("=======================================================")
#         print("1.  Create Table")
#         print("2.  Print Table")
#         print("3.  Get Table")
#         print("4.  Add User")
#         print("5.  Delete User")
#         print("6.  Get Score")
#         print("7.  Update User")
#         print("8.  Change Password")
#         print("9.  Verify User")
#         print("10. Leader Board")
#         print("11. Increment Add")
#         print("12. Increment Sub")
#         print("13. Increment Multi")
#         print("14. Increment Div")
#         print("15. Set Add")
#         print("16. Set Sub")
#         print("17. Set Multi")
#         print("18. Set Div")
#         print("19. Get Add")
#         print("20. Get Sub")
#         print("21. Get Multi")
#         print("22. Get Div")
#         print("*******************************************************")
#         print("0.  Exit")
#         print("")

#         try:
#             selection = int(input("Enter choice(Exit 0): "))
#         except(ValueError):
#             selection = -1
            
#         if selection == 0:
#             break

#         # Creates the DB and Table
#         elif selection == 1:
#             createTable()
#         # Print the tables contents
#         elif selection == 2:
#             printTable()
#         elif selection == 3:
#             data = getTable()
#             print("|Username            |     ADD|     SUB|   MULTI|     DIV|")
#             print("|--------------------+--------+--------+--------+--------+")
#             for row in data:
#                 print('|{0:20}|{2:8}|{2:8}|{2:8}|{2:8}|'.format(row[0],row[1],row[2],row[3],row[4]))
#         # Add a user to the DB
#         elif selection == 4:
#             username =input("User Name: ")
#             password =input("Password: ")
#             addUser(username, password)
#         # Delete a User form the DB
#         elif selection == 5:
#             username =input("User Name: ")
#             deleteUser(username)
#         # Get a Users Score
#         elif selection == 6:
#             username = input("User Name: ")
#             USERS = getScore(username)
#             print ("add_score =   {0}".format(USERS[0]))
#             print ("sub_score =   {0}".format(USERS[1]))
#             print ("multi_score = {0}".format(USERS[2]))
#             print ("div_score =   {0}".format(USERS[3]))
#         # Update a Users Info
#         elif selection == 7:
#             username = input("User Name:")
#             add = float(input("Add Score:"))
#             sub = float(input("Sub Score:"))
#             multi = float(input("Multi Score:"))
#             div = float(input("Div Score:"))
#             USERS = (add,sub,multi,div)
#             updateUser(username, USERS)
#         # Change Users Password
#         elif selection == 8:
#             username = input("User Name: ")
#             password = input("Password: ")
#             changePass(username, password)
#         # Verify a Username and Password
#         elif selection == 9:
#             username = input("User Name: ")
#             password = input("Password: ")
#             if (verifyUser(username, password)):
#                 print ("Valid User")
#             else:
#                 print ("Invalid User")
#         # Get top 5 USERS
#         elif selection == 10:
#             lead = leaderBoard(5)
#             for row in lead:
#                 print ("-------------------------------")
#                 print ("id =          {0}".format(row[0]))
#                 print ("add_score =   {0}".format(row[1]))
#                 print ("sub_score =   {0}".format(row[2]))
#                 print ("multi_score = {0}".format(row[3]))
#                 print ("div_score =   {0}".format(row[4]))
#         # Incrementing the Add Score
#         elif selection == 11:
#             username =input("User Name: ")
#             value = float(input("Inc Amount: "))
#             incAdd(username,value)
#         # Incrementing the Sub Score
#         elif selection == 12:
#             username =input("User Name: ")
#             value = float(input("Inc Amount: "))
#             incSub(username,value)
#         # Incrementing the Multi Score
#         elif selection == 13:
#             username =input("User Name: ")
#             value = float(input("Inc Amount: "))
#             incMulti(username,value)
#         # Incrementing the Div Score
#         elif selection == 14:
#             username =input("User Name: ")
#             value = float(input("Inc Amount: "))
#             incDiv(username,value)
#         # Set the Add Score
#         elif selection == 15:
#             username =input("User Name: ")
#             value = float(input("New Amount: "))
#             setAdd(username,value)
#         # Set the Sub Score
#         elif selection == 16:
#             username =input("User Name: ")
#             value = float(input("New Amount: "))
#             setSub(username,value)
#         # Set the Multi Score
#         elif selection == 17:
#             username =input("User Name: ")
#             value = float(input("New Amount: "))
#             setMulti(username,value)
#         # Set the Div Score
#         elif selection == 18:
#             username =input("User Name: ")
#             value = float(input("New Amount: "))
#             setDiv(username,value)
#         # Get the Add Score
#         elif selection == 19:
#             username =input("User Name: ")
#             value = getAdd(username)
#             print ("Add Score: {0}".format(value))
#         # Get the Sub Score
#         elif selection == 20:
#             username =input("User Name: ")
#             value = getSub(username)
#             print ("Sub Score: {0}".format(value))
#         # Get the Multi Score
#         elif selection == 21:
#             username =input("User Name: ")
#             value = getMulti(username)
#             print ("Multi Score: {0}".format(value))
#         # Get the Div Score
#         elif selection == 22:
#             username =input("User Name: ")
#             value = getDiv(username)
#             print ("Div Score: {0}".format(value))
#         else:
#             print ("not a valid input")
            

#         input("Press Enter to continue")


#******************************************************************************
# Application Main
#******************************************************************************
if __name__ == '__main__':
    Main()
