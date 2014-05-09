from flask import Flask
import couchdb 
from couchdb.client import Server

no_users = 0

app = Flask(__name__)

def init_couchdb():
	server = Server()
	try:
	    db = server.create('pinterest')
	except Exception:
	    db = server['pinterest']
	return db

#Database to Enter Detais
def user_signup(User):
    print "User Signup"
    emailId = User['email']
    db = init_couchdb()
    for docid in  db :
        user = db.get(docid)
        if(user['email'] == emailId):
            print "User already Registered. Please proceed to SignIn"
            return user['user_id']

    print "New User"
    User.store(db)
    return User['user_id']

def user_signin(email,pwd):
    print "User_Sign_in"
    db = init_couchdb()
    for docid in db:
        user = db.get(docid)
        if ( user['email'] == email and user['password'] == pwd ):
            return user['user_id']
    return "Email & Password don't match"


def board_details(user_id,boardName,boardDesc,category,isPrivate,):
	print "Create Board"

