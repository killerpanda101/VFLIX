from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from website.models import Movies

class AddMovieForm(FlaskForm):
	name = StringField("Movie Name", validators=[DataRequired(), Length(min=2, max=20)])
	description = StringField("Movie Description", validators=[DataRequired(), Length(min=2, max=200)])
	picture = FileField('Picture', validators=[DataRequired(), FileAllowed(['jpg','png'])])
	link = StringField("link", validators=[DataRequired(), Length(min=2, max=100)])
	submit = SubmitField("Add Movie")

	def validate_name(self, name):
		movie = Movies.query.filter_by(title =name.data).first()
		if movie:
			raise ValidationError('That movie is already in the database')

class RemoveMovieForm(FlaskForm):
	name = StringField("Movie Name", validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField("Remove Movie")