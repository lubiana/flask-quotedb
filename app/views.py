from flask import render_template, redirect, flash, session, url_for, \
	request, g
from flask.ext.login import login_user, logout_user, current_user, \
	login_required
from app import app, db, lm
from models import User, Quote, ROLE_ADMIN, ROLE_USER, STATUS_ACTIVE, \
	STATUS_INACTIVE
from forms import LoginForm, QuoteForm, RegisterForm, ChangePasswordForm
from datetime import datetime
from decorators import admin_required

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
	quotes = Quote.query.all()
	return render_template('index.html',
		title='Home',
		quotes=quotes)

@app.route('/newQuote', methods=['GET', 'POST'])
@login_required
def newQuote():
	form = QuoteForm()
	if form.validate_on_submit():
		quote = Quote(body=form.quote.data, user_id=g.user.id)
		db.session.add(quote)
		db.session.commit()
		flash('Qoute saved')
		return redirect(url_for('index'))
	return render_template('newQuote.html',
			title='New Quote',
			form=form)

@app.route('/deleteQuote/<int:quote_id>')
@login_required
def deleteQuote(quote_id):
	quote = Quote.query.get(quote_id)
	if quote is None:
		flash('unknown quote')
	elif quote.user_id == g.user.id or g.user.is_admin:
		db.session.delete(quote)
		db.session.commit()
		flash('quote deleted')
	else:
		flash('not authorized')
	return redirect(url_for('index'))
			
@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('You are now registered')
		return redirect(url_for('index'))
	return render_template('register.html',
		title='Register',
		form=form)
        
@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		g.user.set_password(form.new_password.data)
		db.session.add(g.user)
		db.session.commit()
		flash('password has been changed')
		return redirect(url_for('index'))
	return render_template('profile.html',
		title='Profile',
		form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		login_user(form.user)
		flash('logged in')
		return redirect(url_for('index'))
	return render_template('login.html',
		title = 'Login',
		form = form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('you are logged out')
	return redirect(url_for('login'))

@app.route('/admin')
@login_required
@admin_required
def admin():
	users = User.query.all()
	return render_template('admin.html',
		title='Admin Interface',
		users=users)

@app.route('/admin/<action>/<int:user_id>')
@login_required
@admin_required
def admin_action(action, user_id):
	user = User.query.get(user_id)
	if user is not None:
		if action == 'make_admin':
			user.role = ROLE_ADMIN
		elif action == 'make_user':
			user.role = ROLE_USER
		elif action == 'make_active':
			user.active = STATUS_ACTIVE
		elif action == 'make_inactive':
			user.active = STATUS_INACTIVE
		else:
			flash('action not implemented')
			return redirect(url_for('admin'))
		flash('User status changed')
		db.session.add(user)
		db.session.commit()
	else:
		flash('user unknown')
	return redirect(url_for('admin'))
	
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

