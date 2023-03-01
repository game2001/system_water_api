import secrets
from ...database.database_instance import db
from datetime import datetime

class UserModel(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	password = db.Column(db.String(128))
	created_at = db.Column(db.DateTime, default=datetime.now())
	updated_at = db.Column(db.DateTime, onupdate=datetime.now())

	def __repr__(self):
		return '<UserModel {}>'.format(self.username)

	def to_dict(self):
		return {
			'id': self.id,
			'username': self.username,
		}
  
	# def get_reset_token(self, expiration=600):
	# 	"""
	# 	Generate a reset token for the user with a given expiration time.

	# 	:param expiration: The expiration time of the token in seconds (default: 600 seconds).
	# 	:return: The reset token as a string.
	# 	"""
	# 	# Generate a random string for the token
	# 	reset_token = secrets.token_urlsafe(32)

	# 	# Set the reset token and expiration time in the user object
	# 	self.reset_token = reset_token
	# 	self.reset_token_expiration = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)

	# 	# Commit the changes to the database
	# 	db.session.commit()

	# 	return reset_token