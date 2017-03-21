from flask import render_template, redirect, url_for, session, Markup, request
from app import app
from .controllers import MembersForm, SignInForm, DFAStoreForm, ManagementForm, CartForm, AuthenticateLogin, GetMemberList, ValidToken, ItemsList

@app.route('/')
@app.route('/index')
def index():
	if session.get('auth_token'):
		if ValidToken(session['auth_token']):
			return redirect(url_for('dfastore'))
		else:
			return redirect(url_for('signin'))
	else:
		return redirect(url_for('signin'))
	return render_template('index.html', title='DFA Store')

@app.route('/signin', methods=["GET", "POST"])
def signin():
	form = SignInForm()
	if form.validate_on_submit():
		AuthToken = AuthenticateLogin(form.email.data, form.password.data)
		if AuthToken:
			session['auth_token'] = AuthToken
			return redirect(url_for('dfastore'))
		
	return render_template('signin.html', title='Sign In', form=form)

@app.route('/dfastore', methods=["GET", "POST"])
def dfastore():
	if request.method == 'POST':
		if 'managers_button' in request.form:
			return redirect(url_for('management'))
		elif 'cart_button' in request.form:
			return redirect(url_for('cart'))
		elif 'add_cart_button' in request.form:
			return redirect(url_for('addtocart'))
		
	form = DFAStoreForm()
	DFAPS = 'XXXX'		
	ItemsTable = ItemsList.getItems(None)
	CartButtonText = '&nbsp;&nbsp;X&nbsp;:&nbsp;Items &nbsp;&nbsp;&nbsp;X&nbsp;:&nbsp;DFAPs'
	CartButton = Markup('<input style="height:100%; width:100%;color:white;background-color:limegreen;" name="cart_button" type="submit" value="' + CartButtonText + '">')
	return render_template('dfastore.html', title='DFA Store', form=form, dfaps=DFAPS, cartbutton=CartButton, itemstable=ItemsTable)

@app.route('/management', methods=["GET", "POST"])
def management():
	if request.method == 'POST':
		if 'return_button' in request.form:
			return redirect(url_for('dfastore'))
		
	form = ManagementForm()
	return render_template('management.html', title='Management', form=form)
			
@app.route('/cart', methods=["GET", "POST"])
def cart():
	if request.method == 'POST':
		if 'return_button' in request.form:
			return redirect(url_for('dfastore'))
		
	form = CartForm()
	return render_template('cart.html', title='CART', form=form)

@app.route('/addtocart', methods=["GET", "POST"])
def addtocart():
	# items added to cart for the user
	# update store data 
	return redirect(url_for('dfastore'))
			
### The members route is a test route
@app.route('/members')
def members():
	form = MembersForm()
	if ValidToken(session['auth_token']):
		i = 0
		for each in GetMemberList(session['auth_token']):
			form.fields.append([i, each])
			i += 1
	else:
		redirect(url_for('signin'))
		
	return render_template('members.html', title='Members', form=form)