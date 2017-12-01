from flask import Flask, request, render_template, jsonify
import DBAPI, uuid, hashlib

APP = Flask(__name__)

@APP.route('/')
def main():
    return render_template('index.html')


@APP.route('/validate-login', methods=['POST'])
def is_val_login():
    conn = DBAPI.sqlite3.connect("myDB.db")
    curs = conn.cursor()

    email = request.form['email']
    password = request.form['password']
    print(email)
    print(password)


    curs.execute('SELECT * FROM USERS WHERE username=?', (email,))
    data = curs.fetchone()

    if data is None:
        return jsonify({'validEmail' : False, 'validPassword' : False, 'role' : ''})

    if (data[1] != hashlib.sha256(password.encode() + data[2].encode()).hexdigest()):
        return jsonify({'validEmail' : True, 'validPassword' : False, 'role' : ''})

    return jsonify({'validEmail' : True, 'validPassword' : True, 'role' : data[3]})


@APP.route('/vote', methods=['POST'])
def vote():
    conn = DBAPI.sqlite3.connect("myDB.db")
    gold = request.form['first']
    silver = request.form['second']
    bronze = request.form['third']

    # TODO Return notification of successful vote
    return 'Notification'


@APP.route('/vote-report', methods=['POST', 'GET'])
def vote_report():
    # TODO 
    return 'Hello'


@APP.route('/site-list', methods=['POST'])
def site_list():
    # TODO
    return


@APP.route('/upload-logins', methods=['POST'])
def upload_logins():
    # TODO 
    return


@APP.route('/upload-sites', methods=['POST'])
def upload_sites():
    # TODO 
    return


if __name__ == "__main__":
    conn = DBAPI.sqlite3.connect("myDB.db")
    # conn.execute('''CREATE TABLE USERS
    #        (username text, hashresult text, salt text, role text)''')
    salt = uuid.uuid4().hex
    hashresult = hashlib.sha256('admin'.encode() + salt.encode()).hexdigest()
    
    username = 'admin'
    role = 'instructor'
    conn.commit()
    DBAPI.addUser(conn, username, hashresult, salt, role)

# conn.execute('''CREATE TABLE STUDENTS
# (username text, siteid text, gold text, silver text, bronze text)''')
    conn.commit()
    APP.run()
