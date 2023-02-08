from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField, 
    SubmitField, 
    ValidationError, 
    )
from wtforms.validators import InputRequired, EqualTo, Length
from wtforms.widgets import TextArea 
from flask_ckeditor import CKEditorField

    #Create Forms
#----------------------------------------------------------------------

    #Create a Login Form Class
class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[InputRequired()])
    password = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

    #Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("Name:", validators=[InputRequired()])
    submit = SubmitField("Submit")

    #Create a Password Form Class
class PasswordForm(FlaskForm):
    email = EmailField("Email:", validators=[InputRequired()])
    password_hash = PasswordField("Password:", validators=[InputRequired()])
    submit = SubmitField("Submit")

    #Create a Blog Post Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    #content = StringField("Content", validators=[InputRequired()], widget=TextArea())
    content = CKEditorField('Content')
    author = StringField("Author")
    slug = StringField("Slug", validators=[InputRequired()])
    submit = SubmitField("Submit")

    #Create a Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched:", validators=[InputRequired()])
    submit = SubmitField("Submit")

    #Create a User Form Class
class UserForm(FlaskForm):
    name = StringField("Name:", validators=[InputRequired()])
    username = StringField("Username:", validators=[InputRequired()])
    email = StringField("Email:", validators=[InputRequired()])
    favorite_color = StringField("Favorite Color:")
    password_hash = PasswordField(
        "Password", 
        validators=[InputRequired(), 
        EqualTo('password_hash2', message='Passwords must match!')]
        )
    password_hash2 = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Submit")
