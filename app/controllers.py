import requests

from flask_wtf import FlaskForm
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

class MembersForm(FlaskForm):
	fields = []

	members = SelectField('',choices=fields)
	
class SignInForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	
class DFAStoreForm(FlaskForm):
	dfaps = 0

class CartForm(FlaskForm):
	placeholder = 0
	
class ManagementForm(FlaskForm):
	placeholder = 0
	
class Item(object):
	ItemImage = None
	ItemName = ''
	ItemAmount = 0
	ItemCost = 0
	ItemStats = ''
	
	def __init__(self,ItemImage,ItemName,ItemAmount,ItemCost,ItemStats):
		self.ItemImage = ItemImage
		self.ItemName = ItemName
		self.ItemAmount = ItemAmount
		self.ItemCost = ItemCost
		self.ItemStats = ItemStats
			
class ItemsList(object):
	def getItems(self):
		# query items from database here
		Items = []
		# iterate query of items and add the items list
		
		NewItem = Item(None, "Item1", "1", "1", "Stats1")
		Items.append(NewItem)
		NewItem = Item(None, "Item2", "2", "2", "Stats2")
		Items.append(NewItem)
		
		if not Items:
			return "No Items Currently Available in the DFA Store!"
		return Items
	