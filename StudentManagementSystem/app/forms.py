# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age')
    submit = SubmitField('Submit')

class GradeForm(FlaskForm):
    subject = StringField('Subject')
    grade = StringField('Grade')
    submit = SubmitField('Add Grade')
