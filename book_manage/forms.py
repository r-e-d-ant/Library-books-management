from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError
from book_manage.models import Admin

# Register forms
class RegistrationForm(FlaskForm):
    username = StringField('Full name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Register')
    
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
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    submit = SubmitField('Login')


# Upload forms
class Upload(FlaskForm):
    title = StringField('Book title', validators=[DataRequired()])
    author = StringField('Book author')
    description = TextAreaField('Book description')
    
    submit = SubmitField('Register the book')
    

    
# Borrow forms
class Borrow(FlaskForm):
    customer = StringField('Customer name', validators=[DataRequired()])
    title = StringField('Book title', validators=[DataRequired()])
    author = StringField('Book author')
    borrow_date = DateField('Borrow date')
    return_date = DateField('Return date')
    
    submit = SubmitField('Borrow')
