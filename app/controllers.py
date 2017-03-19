import requests

from flask_wtf import Form
from flask import json
from wtforms import SelectField, StringField, PasswordField
from wtforms.validators import DataRequired, Email

def AuthenticateLogin(email, password):
	_ShivtrURL = 'http://dontfeedtheanimals.shivtr.com/'
	_SignInAction = 'users/sign_in.json'
	_Headers = {'Content-Type' : 'application/json'}
	_ShivtrAccount = { "user": { "email": email, "password": password } }
	
	response = requests.post(_ShivtrURL + _SignInAction , data=json.dumps(_ShivtrAccount), headers=_Headers)
	data = response.json()
	if data['user_session']['authentication_token']: 
		return data['user_session']['authentication_token']
	return ''

def ValidToken(authtoken):
	response = UseAuthToken('members.json', authtoken)
	data = response.json()
	if data:
		for each in data['members']:
			if each['display_name']:
				return True
	return False
	
def UseAuthToken(action, authtoken):
	_ShivtrURL = 'http://dontfeedtheanimals.shivtr.com/'
	_Headers = {'Content-Type' : 'application/json'}
	
	return requests.get(_ShivtrURL + action + '?auth_token=' + authtoken)
	
def GetMemberList(authtoken):
	response = UseAuthToken('members.json', authtoken) 
	data = response.json()
	if data:
		memberlist = []
		for each in data['members']:
			memberlist.append(each['display_name'])

	return memberlist

class MembersForm(Form):
	fields = []

	members = SelectField('',choices=fields)
	
class SignInForm(Form):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])