from functools import wraps
from flask import g, request, redirect, url_for, flash
from models import ROLE_ADMIN, User

def admin_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if g.user.role != ROLE_ADMIN:
			flash('not authorized')
			return redirect(url_for('index'))
		return f(*args, **kwargs)
	return decorated_function

