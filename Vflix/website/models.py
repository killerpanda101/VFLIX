from datetime import datetime
from website import db

class Movies(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), unique=True, nullable=False)
	description = db.Column(db.Text, nullable=False)
	photo = db.Column(db.Text, nullable=False)
	link = db.Column(db.Text, nullable=False, unique=True)

	def __repr__(self):
		return f"Movies('{self.title}','{self.description})"



	

	