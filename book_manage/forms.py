from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from book_manage.models import Admin

# Register forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('SignUp')
    
    def validate_username(self, username):
        admin = Admin.query.filter_by(username=username.data).first()
        if admin:
            raise ValidationError('That username is taken. Please choose a different one')
        
    def validate_email(self, email):
        admin = Admin.query.filter_by(email=email.data).first()
        if admin:
            raise ValidationError('That email is taken. Please choose a different one')
        

# Login forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Login')


# Upload forms
class Upload(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author')
    description = TextAreaField('Description')
    
    submit = SubmitField('Save')
    

    
# Borrow forms
class Borrow(FlaskForm):
    customer = StringField('Customer', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author')
    borrow_date = DateField('Borrow date')
    return_date = DateField('Return date')
    
    submit = SubmitField('Borrow')
