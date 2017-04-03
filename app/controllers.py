import requests
from app import models
from flask_wtf import FlaskForm
from flask import json
from wtforms import SelectField, StringField, PasswordField
from wtforms.validators import DataRequired, Email

######
# Authenticate Login
# JSON call to http://dontfeedtheanimals.shivtr.com/users/sign_in.json 
#	passing the email and password to authenticate.
# Returns the authentication Token
######
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

######
# Use Authentication Token
# Takes a passed in action and existing token and perform a 
#	request to the Shivtr.com web site.
# Returns JSON result from the Shivtr.com web site.
######
def UseAuthToken(action, authtoken):
	_ShivtrURL = 'http://dontfeedtheanimals.shivtr.com/'
	_Headers = {'Content-Type' : 'application/json'}
	
	return requests.get(_ShivtrURL + action + '?auth_token=' + authtoken)

######
# Validate Token
# Takes a passed in token id and validates it against Shivtr.com 
#	web site using the UseAuthToken function to verify if still active.
# Returns True or False depending if it is able to retrieve a list 
#	of members from Shivtr.com web site.
######
def ValidToken(authtoken):
	response = UseAuthToken('members.json', authtoken)
	data = response.json()
	if data:
		for each in data['members']:
			if each['display_name']:
				return True
	return False
	
def GetMemberList(authtoken):
	response = UseAuthToken('members.json', authtoken) 
	data = response.json()
	if data:
		memberlist = []
		for each in data['members']:
			memberlist.append(each['display_name'])

	return memberlist
	
class SignInForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	
class DFAStoreForm(FlaskForm):
	dfaps = 0

class CartForm(FlaskForm):
	placeholder = 0
	
class ManagementForm(FlaskForm):
	placeholder = 0
	
class UserManagementForm(FlaskForm):
	memberlist = []
	dfaps = 0
	manualedit = False

	members = SelectField('Members', choices=memberlist)
	
	def UpdateFormData(self, Member):
		Member = models.Members.GetMember(models.Members, Member)
		if Member and Member.dfaps:
			UserManagementForm.dfaps = Member.dfaps
		else: 
			UserManagementForm.dfaps = 0

	def GetMembersList(self):
		Members = models.Members.GetAllMembers(models.Members)
		UserManagementForm.memberlist.clear()
		UserManagementForm.memberlist.append([0, ''])
		i = 1
		for Member in Members:
			UserManagementForm.memberlist.append([i, Member.name])
			i += 1
		
	def UpdateMembersList(self, AuthToken):
		response = UseAuthToken('members.json', AuthToken)
		data = response.json()
		for member in data['members']:
			if not models.Members.GetMember(models.Members, member['display_name']):
				models.Members.AddMember(models.Members, member['display_name'])
				
	def SaveMemberData(self, Member, DFAPs, Increment):
		models.Members.UpdateMember(models.Members, Member, DFAPs, Increment)
		
class ShopManagementForm(FlaskForm):
	placeholder = 0
	
class EditStoreItemForm(FlaskForm):
	memberlist = []
	itemlist = []
	imagelist = []
	
	items = SelectField('Items', choices=itemlist)
	members = SelectField('Members', choices=memberlist)
	images = SelectField('Images', choices=imagelist)
	
class CartManagementForm(FlaskForm):
	activecarts = 0
	memberlist =[]
	itemlist = []
	itemsincart = 0
	
	members = SelectField('Members', choices=memberlist)
	items = SelectField('Items', choices=itemlist)
	
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
	