from flask import (
  Blueprint,
  request
)

from applause import db

from applause.model import (
  Clap,
  PageView,
  Page,
  Key
)

from applause.forms import (
  CreateClapForm,
  UpdateClapForm
)

import datetime

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

# for getting the remote address if this app is running behind a reverse proxy
def get_remote_addr(request):
  if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    return request.environ['REMOTE_ADDR']
  else:
    return request.environ['HTTP_X_FORWARDED_FOR']

@bp.route('/clap', methods=['POST','PUT'])
def clap():
  # for the first time a user claps, a POST request is sent
  if request.method == 'POST':
    form = CreateClapForm()
    if form.validate_on_submit():
      form_path = form.path.data
      form_key = form.key.data
      ip = get_remote_addr(request)
      # create a new clap record
      # look up the page using the key and the page path
      # need to revisit the database design because this query is v expensive
      page = Key.query.filter_by(uuid=form_key).first().domain.pages.filter_by(path=form_path).first()
      # the page should exist since it is created when the page is viewed, but check anyway
      if page is not None:
        new_clap = Clap(pid=pid, ip=ip)
        db.session.add(new_clap)
        db.session.commit()
        return ('', 200)
  # subsequent claps (updates to the number of claps) are sent with a PUT request
  elif request.method == 'PUT':
    form = UpdateClapForm()
    if form.validate_on_submit():
      form_path = form.path.data()
      num_claps = form.num_claps.data
      form_key = form.key.data
      ip = get_remote_addr(request)
      # update a clap record with the number of claps
      # look up the clap using the key, ip, and page path
      # need to revisit the database design because this query is v expensive
      clap = Key.query.filter_by(uuid=form_key).first().domain.pages.filter_by(path=form_path).first().claps.filter_by(ip=ip).first()
      if clap is not None:
        clap.num_claps = num_claps
        db.session.commit()
        return ('', 200)
  return ('', 400)

# creates a pageview record, or updates it when a user leaves a page
@bp.route('/view', methods=['POST', 'PUT'])
def view():
  # a PUT request creates a page view record
  if request.method == 'POST':
    form_path = request.form['path']
    form_referrer = request.form['referrer']
    form_key = request.form['key']
    ip = get_remote_addr(request)
    # look up the page using the path and key
    page = Key.query.filter_by(uuid=form_key).first().domain.pages.filter_by(path=form_path).first()
    # if the page does not exist, create it
    if page is None:
      # look up the did with the key
      did = Key.query.filter_by(uuid=form_key).first().domain.did
      new_page = Page(did=did, path=form_path)
      db.session.add(new_page)
      db.session.commit()
      page = new_page
    # create the page view record
    new_page_view = PageView(pid=page.pid, ip=ip, referrer=form_referrer)
    db.session.add(new_page_view)
    db.session.commit()
    return (str(new_page_view.pvid), 200)
  # a PUT request updates a page view record with the page view duration
  elif request.method == 'PUT':
    form_path = request.form['path']
    form_pvid = request.form['pvid']
    form_key = request.form['key']
    # look up the page view by pvid
    page_view = PageView.query.filter_by(pvid=form_pvid).first()
    if page_view is not None:
      # update the page view with the interval
      start_time = page_view.start_time
      end_time = datetime.datetime.utcnow()
      interval = end_time - start_time
      page_view.time_on_page = interval
      db.session.commit()
      return ('', 200)
  return ('', 400)
