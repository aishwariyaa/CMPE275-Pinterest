from flask import Flask
from flask import request
from flask import Response
import json
import db_util

app = Flask(__name__)

@app.route('/')
def welcome_page():
	return "Welcome to Pinterest !!!"

@app.route('/signup', methods = ['POST'])
def signup():
	user_details = request.get_json()
	firstName = user_details.get('firstName')
	lastName = user_details.get('lastName')
	emailId = user_details.get('emailId')
	password = user_details.get('password')
	print firstName, " : ",lastName, " : ",emailId, " : ",password
	db_util.user_signup(firstName,lastName,emailId,password)
	return "201 User Login Successful !! "


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