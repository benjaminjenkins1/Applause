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

from applause import db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/dashboard', methods=['GET'])
def dashboard():
  return render_template('dashboard.html')