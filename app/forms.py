from flask.ext.wtf import Form, TextField, Required, BooleanField, \
	PasswordField, TextAreaField, EqualTo
from app.models import User, Quote
from flask import g

class LoginForm(Form):
	username = TextField('Username', validators = [Required()])
	password = PasswordField('Password', validators = [Required()])
	remember_me = BooleanField('Remember me', default = False)
	
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None
		
	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False
		
		user = User.query.filter_by(username=self.username.data).first()
		if user is None:
			self.username.errors.append('User does not exist')
			return False
		if not user.is_active():
			self.username.errors.append('User is not activated')
			return False
		if not user.check_password(self.password.data):
			self.password.errors.append('Password is wrong')
			return False
			
		self.user = user
		return True

class QuoteForm(Form):
	quote = TextAreaField('Quote', validators = [Required()])
	
class RegisterForm(Form):
	username = TextField('Username', validators = [Required()])
	password = PasswordField('Password', validators = [Required()])
	confirm = PasswordField('Confirm', validators = [Required(),
		EqualTo('confirm', message='Passwords do not match')])
	
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None
		
	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False
		
		user = User.query.filter_by(username=self.username.data).first()
		if user is not None:
			self.username.errors.append('Username already exists')
			return False
	
		return True
		
class ChangePasswordForm(Form):
	old_password = PasswordField('old password', validators = [Required()])
	new_password = PasswordField('new password', validators = [Required()])
	confirm = PasswordField('confirm', validators = [Required(),
		EqualTo('confirm', message='Passwords do not match')])
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None
	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False
		if not g.user.check_password(self.old_password.data):
			self.username.errors.append('the current password is wrong')
			return False
		return True
