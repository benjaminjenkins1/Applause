from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask import current_app

RECAPTCHA_PUBLIC_KEY = current_app.config['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = current_app.config['RECAPTCHA_PRIVATE_KEY']

email_validator = Email(message='That isn\'t a valid email address')

class RegisterForm(FlaskForm):
  email = StringField('Email address', validators=[email_validator])
  password = PasswordField('Password', validators=[Length(min=8, max=100, message='Your password needs to be between 8 and 100 characters long')])
  confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
  recaptcha = RecaptchaField(validators=[Recaptcha(message="Please complete the captcha")])
  

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[email_validator])
  password = PasswordField('Password', [DataRequired(message='You have to provide a password')])


class AddDomainForm(FlaskForm):
  domain_name = StringField('Domain Name', validators=[DataRequired(message='You have to provide a domain name'), Regexp('^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$', message='This is not a valid domain name')])

class AddKeyForm(FlaskForm):
  did = StringField('Domain ID', validators=[DataRequired()])

class DeleteKeyForm(FlaskForm):
  uuid = StringField('uuid', validators=[DataRequired()])
  did = StringField('did', validators=[DataRequired()])
  