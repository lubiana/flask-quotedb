from app import db
from werkzeug.security import generate_password_hash, \
     check_password_hash
  
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0        
ROLE_USER = 0
ROLE_ADMIN = 1
VOTE_PLUS = 1
VOTE_MINUS = 0

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(10), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	active = db.Column(db.SmallInteger, default = 0)
	password = db.Column(db.String(160))
	last_seen = db.Column(db.DateTime)
	quotes = db.relationship("Quote", 
		backref=db.backref("user", lazy="joined"))
        
	def set_password(self, password):
		self.password = generate_password_hash(password)
			
	def check_password(self, password):
		return check_password_hash(self.password, password)
		
	def is_authenticated(self):
		return True
	
	def is_active(self):
		if self.active == STATUS_ACTIVE:
			return True
		return False 
	
	def is_admin(self):
		if self.role == ROLE_ADMIN:
			return True
		return False
	
	def is_anonymous(self):
		return False
	
	def get_id(self):
		return unicode(self.id)

class Quote(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        body = db.Column(db.Text)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Vote(db.Model):
        vote = db.Column(db.SmallInteger)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
        quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), primary_key = True)

