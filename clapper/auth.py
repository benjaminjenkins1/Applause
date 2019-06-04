from flask import (
  Blueprint,
  flash,
  g,
  redirect,
  render_template,
  request,
  session,
  url_for
)

from werkzeug.security import (
  check_password_hash,
  generate_password_hash
)

from clapper import db

from forms import (
  RegisterForm,
  LoginForm
)

from model import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
  form = RegisterForm()
  if request.method == 'POST' and form.validate():
    email = form.email.data
    pass_hash = generate_password_hash(form.password.data)
    user = User(email=email, pass_hash=pass_hash)
    exists = User.query.filter_by(email=email).first() is not None
    if not exists:
      db.session.add(user)
      db.session.commit()
      session.clear()
      session['email'] = email
      return redirect(url_for('dashboard'))
    else:
      flash('There\'s already an account with that email address')
  return render_template('register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
  form = LoginForm()
  if request.method == 'POST' and form.validate():
    email = form.email.data
    password = form.email.password
    user = User.query.filter_by(email=email).first()
    if not check_password_hash(user.pass_hash, password):
      flash('Incorrect password')
    else:
      session.clear()
      session['email'] = email
      return redirect(url_for('dashboard'))
  return render_template('login.html')


@bp.route('/logout')
def logout():
  session.clear()
  return redirect(url_for('index'))
