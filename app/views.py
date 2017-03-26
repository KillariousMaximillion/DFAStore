from flask import render_template, redirect, url_for, session, Markup, request
from app import app
from .controllers import MembersForm, SignInForm, DFAStoreForm, ManagementForm, UserManagementForm, ShopManagementForm, EditStoreItemForm, CartManagementForm, CartForm, AuthenticateLogin, GetMemberList, ValidToken, ItemsList

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
		if 'dfashop_button' in request.form:
			return redirect(url_for('dfastore'))
		elif 'user_manage_button' in request.form:
			return redirect(url_for('usermanagement'))
		elif 'shop_manage_button' in request.form:
			return redirect(url_for('shopmanagement'))
		elif 'cart_manage_button' in request.form:
			return redirect(url_for('cartmanagement'))
		
	form = ManagementForm()
	
	return render_template('management.html', title='Management', form=form)
			
@app.route('/usermanagement', methods=["GET", "POST"])
def usermanagement():
	form = UserManagementForm()
	ManualEditDFAPs = ''
	
	if not form.fields and ValidToken(session['auth_token']):
		i = 0
		form.fields.append([i, ''])
		i += 1
		for each in GetMemberList(session['auth_token']):
			form.fields.append([i, each])
			i += 1
	else:
		redirect(url_for('signin'))
		
	if request.form.get('members') and (request.form.get('members')).isdigit():
		if form.fields[int(request.form.get('members'))][1] == 'Mystic1':
			form.dfaps = 100
		elif form.fields[int(request.form.get('members'))][1] == 'cambriolage':
			form.dfaps = 200
	
	DFAPS = form.dfaps
	
	if request.method == 'POST':
		if 'dfashop_button' in request.form:
			return redirect(url_for('dfastore'))
		elif 'user_manage_button' in request.form:
			return redirect(url_for('usermanagement'))
		elif 'shop_manage_button' in request.form:
			return redirect(url_for('shopmanagement'))
		elif 'cart_manage_button' in request.form:
			return redirect(url_for('cartmanagement'))
		elif 'manual_edit_button' in request.form:
			form.manualEdit = True
			ManualEditDFAPs = Markup('<input name="manual_dfaps" type="text" value="' + str(form.dfaps) + '">')
		elif 'save_button' in request.form:
			# save dfaps to database here and repost same page
			form.manualEdit = False
			
	return render_template('usermanagement.html', title='User Management', form=form, dfaps=DFAPS, manualeditdfaps=ManualEditDFAPs)

@app.route('/shopmanagement', methods=["GET", "POST"])
def shopmanagement():
	form = ShopManagementForm()
	
	if request.method == 'POST':
		if 'dfashop_button' in request.form:
			return redirect(url_for('dfastore'))
		elif 'user_manage_button' in request.form:
			return redirect(url_for('usermanagement'))
		elif 'shop_manage_button' in request.form:
			return redirect(url_for('shopmanagement'))
		elif 'cart_manage_button' in request.form:
			return redirect(url_for('cartmanagement'))
		elif 'add_new_item_button' in request.form:
			return redirect(url_for('editstoreitem'))
		elif 'edit_item_button' in request.form:
			return redirect(url_for('editstoreitem'))
		
	ItemsTable = ItemsList.getItems(None)	
	return render_template('shopmanagement.html', title='Shop Management', form=form, itemstable=ItemsTable)

@app.route('/editstoreitem', methods=["GET", "POST"])
def editstoreitem():
	form = EditStoreItemForm()
	
	if not form.memberlist and ValidToken(session['auth_token']):
		i = 0
		form.memberlist.append([i, ''])
		i += 1
		for each in GetMemberList(session['auth_token']):
			form.memberlist.append([i, each])
			i += 1
	else:
		redirect(url_for('signin'))
			
	ItemList = ItemsList.getItems(None)
	form.itemlist.clear()
	i = 0
	form.itemlist.append([i, ''])
	i += 1
	for item in ItemList:
		form.itemlist.append([i, item.ItemName])
		i += 1
		
	form.imagelist.clear()
	i = 0
	form.imagelist.append([i, ''])
	i += 1
	form.imagelist.append([i, 'Placeholder Image'])
		
	if request.method == 'POST':
		if 'dfashop_button' in request.form:
			return redirect(url_for('dfastore'))
		elif 'user_manage_button' in request.form:
			return redirect(url_for('usermanagement'))
		elif 'shop_manage_button' in request.form:
			return redirect(url_for('shopmanagement'))
		elif 'cart_manage_button' in request.form:
			return redirect(url_for('cartmanagement'))
		elif 'save_button' in request.form:
			return redirect(url_for('shopmanagement'))
			
	return render_template('editstoreitem.html', title='Edit Store Item', form=form)

@app.route('/cartmanagement', methods=["GET", "POST"])
def cartmanagement():	
	form = CartManagementForm()
	ItemsTable = []

	form.memberlist.clear()
	form.memberlist.append([0, ''])
	form.memberlist.append([1, 'Mystic1'])
	form.memberlist.append([2, 'cambriolage'])
	
	if request.form.get('members') and (request.form.get('members')).isdigit():
		if form.memberlist[int(request.form.get('members'))][1] == 'Mystic1':
			ItemsTable = ItemsList.getItems(None)
			form.itemsincart = len(ItemsTable)
		elif form.memberlist[int(request.form.get('members'))][1] == 'cambriolage':
			ItemsTable = ItemsList.getItems(None)
			form.itemsincart = len(ItemsTable)
		
	if request.method == 'POST':
		if 'dfashop_button' in request.form:
			return redirect(url_for('dfastore'))
		elif 'user_manage_button' in request.form:
			return redirect(url_for('usermanagement'))
		elif 'shop_manage_button' in request.form:
			return redirect(url_for('shopmanagement'))
		elif 'cart_manage_button' in request.form:
			return redirect(url_for('cartmanagement'))
		
	#ItemsTable = ItemsList.getItems(None)
	
	AvailableDFAPS = 'XXXX'
	UsedDFAPS = 'XXXX'
	TotalDFAPS = 'XXXX'
	form.activecarts = 2
		
	return render_template('cartmanagement.html', title='Cart Management', form=form, itemstable=ItemsTable, availabledfaps=AvailableDFAPS, useddfaps=UsedDFAPS, totaldfaps=TotalDFAPS)

@app.route('/cart', methods=["GET", "POST"])
def cart():
	if request.method == 'POST':
		if 'return_button' in request.form:
			return redirect(url_for('cart'))
		elif 'dfashop_button' in request.form:
			return redirect(url_for('dfastore'))
		elif 'managers_button' in request.form:
			return redirect(url_for('management'))
		
	form = CartForm()
	AvailableDFAPS = 'XXXX'
	UsedDFAPS = 'XXXX'
	TotalDFAPS = 'XXXX'
	ItemsTable = ItemsList.getItems(None)
	
	return render_template('cart.html', title='CART', form=form, itemstable=ItemsTable, availabledfaps=AvailableDFAPS, useddfaps=UsedDFAPS, totaldfaps=TotalDFAPS)

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