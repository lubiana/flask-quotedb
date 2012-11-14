from functools import wraps
from flask import g, request, redirect, url_for, flash
from models import User

def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user.is_anonymous():
			flash('user is anonymous')
			return redirect(url_for('index'))
		if not g.user.is_admin():
			flash('not authorized')
			return redirect(url_for('index'))
		return f(*args, **kwargs)
	return decorated_function

