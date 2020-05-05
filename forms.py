from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import IntegerField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('E-Mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField("Content")
    is_private = BooleanField("Private")
    submit = SubmitField('Submit')


class JobForm(FlaskForm):
    title = StringField("Job Title", validators=[DataRequired()])
    leader_id = IntegerField("Team Leader Id", validators=[DataRequired()])
    work_size = IntegerField("WorkSize", validators=[DataRequired()])
    collaborators = StringField("Collaborators", validators=[DataRequired()])
    category = IntegerField("Category Id", validators=[DataRequired()])
    is_finished = BooleanField("Is job finished?")
    submit = SubmitField('Submit')


class DepForm(FlaskForm):
    title = StringField("Department name", validators=[DataRequired()])
    chief_id = IntegerField("Chief Id", validators=[DataRequired()])
    members = StringField("Members", validators=[DataRequired()])
    email = StringField("E-Mail", validators=[DataRequired()])
    submit = SubmitField('Submit')
