from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import current_app

RECAPTCHA_PUBLIC_KEY = current_app.config['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = current_app.config['RECAPTCHA_PRIVATE_KEY']

email_validator = [Email(message='That isn\'t a valid email address')]

class RegisterForm(FlaskForm):
  email = StringField('Email', email_validator)
  password = PasswordField('Password', [EqualTo(confirm_password, message='Passwords must match'), Length(min=8, max=100, message='Your password needs to be between 8 and 100 characters long')])
  confirm_password = PasswordField('Confirm password')
  recaptca = RecaptchaField()
  

class LoginForm(FlaskForm):
  email = StringField('Email', email_validator)
  password = PasswordField('Password', [DataRequired(message='You have to provide a password')])




