import DBAPI, uuid, hashlib, csv, os, zipfile
from flask import Flask, request, render_template, jsonify, send_from_directory, send_file


conn = DBAPI.sqlite3.connect("myDB.db")

app = Flask(__name__)
currentUser = ''
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/templates/<name>', methods=['POST', 'GET'])
def sites(name):
    c = conn.cursor()
    t = (name,)
    c.execute('SELECT * FROM SITES WHERE siteid=?', t)
    data = c.fetchone()
    if (data is None): 
        return 'Error'
    else:
        return send_from_directory('templates/' + name, 'index.html')


@app.route('/validate-login', methods=['POST'])
def is_val_login():
    curs = conn.cursor()

    email = request.form['email']
    password = request.form['password']

    curs.execute('SELECT * FROM USERS WHERE username=?', (email,))
    data = curs.fetchone()
    
    if data is None:
        return jsonify({'validEmail' : False, 'validPassword' : False, 'role' : ''})

    if (data[1] != hashlib.sha256(password.encode() + data[2].encode()).hexdigest()):
        return jsonify({'validEmail' : True, 'validPassword' : False, 'role' : ''})
    
    currentUser = email
    return jsonify({'validEmail' : True, 'validPassword' : True, 'role' : data[3]})


@app.route('/vote', methods=['POST'])
def vote():
    first = request.form['gold']
    second = request.form['silver']
    third = request.form['bronze']

    user = currentUser

    DBAPI.addVote(conn, user, first, second, third)


@app.route('/get-votes', methods=['POST', 'GET'])
def vote_report():

    

    with open('vote-report.csv', 'wb') as f:
        cur = conn.cursor()
        for row in cur.execute('SELECT * FROM VOTEREPORT'):
            writeRow = " ".join([str(i) for i in row])
            f.write(writeRow.encode())

    return send_file('vote-report.csv',
                     mimetype='text/csv',
                     attachment_filename='vote-report.csv',
                     as_attachment=True)


@app.route('/site-list', methods=['POST', 'GET'])
def site_list():

    cur = conn.cursor()

    cur.execute('SELECT * FROM SITES')
    tablen = cur.fetchall()
    newtable = []

    for row in tablen:
        mydict = {}
        mydict['id'] = row[0]
        mydict['url'] = row[1]
        newtable.append(mydict)

    return jsonify(newtable)


@app.route('/upload-logins', methods=['POST'])
def upload_logins():
    f = request.files['file']

    cur = conn.cursor()

    filename = f.filename

    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as ft:
        dr = csv.DictReader(ft)
        salt = uuid.uuid4().hex
        to_db = [(i['username'], (hashlib.sha256((i['password']).encode() + salt.encode()).hexdigest()), salt, i['role']) for i in dr]

    cur.executemany("INSERT INTO USERS (username, hashresult, salt, role) VALUES (?, ?, ?, ?);", to_db)
    conn.commit()

    return render_template('index.html')


@app.route('/upload-sites', methods=['POST'])
def upload_sites():
    f = request.files['file']

    cur = conn.cursor()

    filename = f.filename
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    with zipfile.ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as ft:
        names = ft.namelist()
        ft.extractall(os.path.join(app.root_path + '/templates'))
        for name in names:
            if name[-4:] == 'html':
                ind = name.index("/")
                student = name[:ind]
                DBAPI.addSite(conn, student, student)

    return render_template('index.html')


if __name__ == "__main__":

    DBAPI.createUsers(conn)
    DBAPI.createVoteReport(conn)
    DBAPI.createSites(conn)

    salt = uuid.uuid4().hex
    hashresult = hashlib.sha256('admin'.encode() + salt.encode()).hexdigest()
    username = 'admin'
    role = 'instructor'
    DBAPI.addUser(conn, username, hashresult, salt, role)
    conn.commit()

    app.run()
