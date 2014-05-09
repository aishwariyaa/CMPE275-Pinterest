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


def incr_user_count():
	global no_users
	no_users = no_users + 1
	return no_users

#Database to Enter Detais
def user_signup(firstName,lastName,emailId,password):
	print "User Signup"
	db = init_couchdb()
	for docid in  db :
		user = db.get(docid)
		if(user['emailId'] == emailId):
			print "User already Registered. Please proceed to SignIn"
			return 0

	print "New User"
	doc = {'firstName':firstName , 'lastName':lastName, 'emailId':emailId , 'password':password , 'user_id':incr_user_count()}
	db.save(doc)
	return 0


def board_details(boardName,boardDesc,category,isPrivate,):
	print "Create Board"


if __name__ == '__main__':
	user_signup('Gayathri','Srinivasan','gaya1.0408@gmail.com','abcd')
	app.run(debug=True)