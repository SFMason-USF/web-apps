import json
from flask import Flask, request, render_template
import DBAPI

APP = Flask(__name__)


@APP.route('/')
def main():
    return render_template('index.html')

# TODO check if needed
# @APP.route('/')
# def main():
#     return render_template('other.html')

@APP.route('/sign-up.html')
def sign_up():
    return render_template('sign-up.html')

@APP.route('/validate-login', methods=['POST'])
def is_val_login():
    conn = DBAPI.sqlite3.connect("myDB.db")
    new_user = request.form['newUser']
    email = request.form['email']
    password = request.form['password']

    if new_user:
        conf = DBAPI.addUser(conn, email, password)
        #TODO return confirmation of added user
        return 'Confirmation'
    else:
        # TODO Check if valid email and pw

        # TODO Get role
        role = 'role'
        return json.dumps({'validEmail':True, 'validPassword':True, 'role':role})

@APP.route('/vote', methods=['POST'])
def vote():
    conn = DBAPI.sqlite3.connect("myDB.db")
    first_vote = request.form['first']
    second_vote = request.form['second']
    third_vote = request.form['third']

    # TODO Return notification of successful vote
    return 'Notification'

@APP.route('/vote-report', methods=['POST'])
def vote_report():
    #TODO 
    return

@APP.route('/site-list', methods=['POST'])
def site_list():
    return

if __name__ == "__main__":
    APP.run()