from flask import render_template, redirect, url_for, session
from app import app
from .controllers import MembersForm, SignInForm, AuthenticateLogin, GetMemberList, ValidToken

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
	return render_template('dfastore.html', title='DFA Store')

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