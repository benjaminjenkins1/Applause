from flask import (
  Blueprint,
  flash,
  g,
  redirect,
  render_template,
  request,
  session,
  url_for,
  Markup
)

from werkzeug.security import (
  check_password_hash,
  generate_password_hash
)

from applause import db

from applause.model import User

from applause.forms import (
  RegisterForm,
  LoginForm
)

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
  # view decorator that redirects anonymous users to the login page
  @functools.wraps(view)
  def wrapped_view(**kwargs):
    if g.user is None:
      return redirect(url_for('auth.login'))
    return view(**kwargs)
  return wrapped_view

@bp.before_app_request
def load_logged_in_user():
  # if a user email is stored in the session
  # load the user object from the database into g.user
  user_email = session.get('email')
  if user_email is None:
    g.user = None
  else:
    g.user = User.query.filter_by(email=user_email).first()

@bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm()
  if form.is_submitted() and form.validate_on_submit():
    email = form.email.data
    pass_hash = generate_password_hash(form.password.data)
    user = User(email=email, pass_hash=pass_hash)
    exists = User.query.filter_by(email=email).first() is not None
    if not exists:
      db.session.add(user)
      db.session.commit()
      session.clear()
      session['email'] = email
      return redirect(url_for('dashboard.dashboard'))
    else:
      msg = Markup('There\'s already an account with that email address<br><a href="/auth/login">Log in</a><br><a href="/auth/reset_password">Reset password</a>')
      flash(msg)
  return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm(request.form)
  if request.method == 'POST' and form.validate():
    email = form.email.data
    password = form.password.data
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.pass_hash, password):
      flash('Incorrect password')
    else:
      session.clear()
      session['email'] = email
      return redirect(url_for('dashboard.dashboard'))
  return render_template('auth/login.html', form=form)

@bp.route('/reset_password', methods=['GET','POST'])
def reset_password():
  return render_template('auth/reset_password.html')


@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))
