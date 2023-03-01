import secrets
from ...database.database_instance import db
from datetime import datetime

class ProblemModel(db.Model):
	__tablename__ = 'problems'
	id = db.Column(db.Integer, primary_key=True)
	desc = db.Column(db.Text, nullable=False)
	lat = db.Column(db.Numeric(precision=20, scale=15), nullable=False)
	lng = db.Column(db.Numeric(precision=20, scale=15), nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.now())
	updated_at = db.Column(db.DateTime, onupdate=datetime.now())

	def __repr__(self):
		return '<ProblemModel {}>'.format(self.id)

	def to_dict(self):
		return {
			'id': self.id,
			'desc': self.desc,
		}
  