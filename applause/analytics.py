from flask import (
  Blueprint,
  request
)

from applause import db

from applause.model import (
  Clap,
  PageView
)

from applause.forms import (
  ClapForm,
  PageViewForm,
  LeavePageForm
)

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

# for getting the remote address if this app is running behind a reverse proxy
def get_remote_addr(request):
  if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    return request.environ['REMOTE_ADDR']
  else:
    return request.environ['HTTP_X_FORWARDED_FOR']

@bp.route('/clap', methods=['POST','PUT'])
def clap():
  form = ClapForm()
  if form.validate_on_submit():
    page = form.page.data
    ip = get_remote_addr(request)
    # for the first time a user claps, a POST request is sent
    if request.method == 'POST':

    # subsequent claps (updates to the number of claps) are sent with a PUT request
    elif request.method == 'PUT':

# creates a pageview record
@bp.route('/view', methods=['POST'])
def leave():


# updates a pageview record with the time the user was on the page
@bp.route('/leave', methods=['PUT'])
def leave():