from flask import Flask
from flask import request
from flask import Response
import json
import db_util

no_users = 0

app = Flask(__name__)

def incr_user_count():
    global no_users
    no_users = no_users + 1
    return no_users

class User(Document):
    firstName = TextField()
    lastName = TextField()
    email = TextField()
    password = TextField()
    user_id = TextField()
    boards = TextField()

@app.route('/')
def welcome_page():
	return "Welcome to Pinterest !!!"

#Database to Enter Detais
@app.route("/user/add", methods=['POST'])
def user_signup():
    user_details = request.get_json()
    fname = user_details.get('fname')
    lname = user_details.get('lname')
    emailID = user_details.get('email')
    passwd = user_details.get('password')
    print "User Signup"
    new_user = User(firstName=fname, lastName=lname, email=emailID, password=passwd, user_id=incr_user_count(),
                    boards="0")
    user_id = db_util.user_signup(new_user)
    print user_id
    #return user_id
    if (user_id != "0"):
        links = {'links': [
            {'url': '/user/login', 'method': 'POST'},
        ],'userID' : user_id}
        js = json.dumps(links)
        resp = Response(js, status=201, mimetype='application/json')
        resp.headers['Link'] = 'http://127.0.0.1:5000'
        return resp

@@app.route('/user/login', methods=['POST'])
def login():
    user_details = request.get_json()
    emailID = user_details.get('email')
    passwd = user_details.get('password')

    message = db_util.user_signin(emailID, passwd)
    if (message != "Email & Password don't match"):
        links = {'links': [
            {'url': '/user/{user_id}/boards', 'method': 'GET'},
            {'url': '/user/{user_id}/boards', 'method': 'POST'},
        ],'userID' : user_id}
        js = json.dumps(links)
        resp = Response(js, status=201, mimetype='application/json')
        resp.headers['Link'] = 'http://127.0.0.1:5000'
        return resp
    return "Email & Password don't match"


@app.route('/user/<int:user_id>/boards/', methods = ['POST'])
def boards(user_id):
	print 'User Id %d' % user_id
	board_details = request.get_json()
	boardName = board_details.get('boardName')
	boardDesc = board_details.get('boardDesc')
	category = board_details.get('category')
	isPrivate = board_details.get('isPrivate','False')
	db_util.board_details(user_id,boardName,boardDesc,category,isPrivate)
	# Return List of Allowed Operations

	links = {'links' : [
				{'url' : '/users/{UserId}/boards/{boardName}','method': 'GET'},
				{'url' : 'users/{UserId}/boards/{boardName}/','method': 'PUT'},
				{'url' : 'users/{UserId}/boards/{boardName}/','method': 'DELETE'},
				{'url' : 'users/{UserId}/boards/{boardName}/pins','method': 'POST'}
			]}

	js= json.dumps(links)
	resp = Response(js, status=201, mimetype='application/json')
	resp.headers['Link'] = 'http://127.0.0.1:5000'
	#return "201 User Login Successful !! "
	return resp

if __name__ == '__main__':
    app.run(debug=True)