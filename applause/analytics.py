from flask import (
  Blueprint,
  request,
  jsonify
)

from applause import db

from applause.model import (
  Clap,
  PageView,
  Page,
  Key
)

from sqlalchemy.sql import func

from flask_cors import cross_origin

import datetime

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

# for getting the remote address if this app is running behind a reverse proxy
def get_remote_addr(request):
  if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    return request.environ['REMOTE_ADDR']
  else:
    return request.environ['HTTP_X_FORWARDED_FOR']

@bp.route('/clap', methods=['POST','PUT','GET'])
@cross_origin()
def clap():
  # for the first time a user claps, a POST request is sent
  if request.method == 'POST':
    form_path = request.form['path']
    form_key = request.form['key']
    ip = get_remote_addr(request)
    # create a new clap record
    # look up the page using the key and the page path
    # need to revisit the database design because this query is probably slow
    page = Key.query.filter_by(uuid=form_key).first().domain.pages.filter_by(path=form_path).first()
    # the page should exist since it is created when the page is viewed, but check anyway
    if page is not None:
      # Clap is initialized with num_claps=1
      new_clap = Clap(pid=page.pid, ip=ip)
      db.session.add(new_clap)
      db.session.commit()
      return ('', 200)
  # subsequent claps (updates to the number of claps) are sent with a PUT request
  elif request.method == 'PUT':
    form_path = request.form['path']
    num_claps = int(request.form['num_claps'])
    if num_claps > 50 or num_claps < 1:
      return ('', 400)
    form_key = request.form['key']
    ip = get_remote_addr(request)
    # update a clap record with the number of claps
    # look up the clap using the key, ip, and page path
    # need to revisit the database design because this query is v expensive
    clap = Key.query.filter_by(uuid=form_key).first().domain.pages.filter_by(path=form_path).first().claps.filter_by(ip=ip).first()
    if clap is not None:
      clap.num_claps = num_claps
      db.session.commit()
      return ('', 200)
  # For getting the number of claps when the page loads
  # Returns the total number of claps and the claps by this specific user
  elif request.method == 'GET':
      form_path = request.form['path']
      print(form_path)
      form_key = request.form['key']
      user_ip = get_remote_addr(request)
      # query the database for the total number of claps, then filter for this user's claps
      # this is probably very slow and should be improved
      all_claps = Key.query.filter_by(uuid=form_key).first().domain.pages.filter_by(path=form_path).first().claps
      all_claps_list = all_claps.all()
      # fix this garbage:
      total_num_claps = 0
      for clap in all_claps:
        total_num_claps += clap.num_claps
      user_claps = all_claps.filter_by(ip=user_ip).first()
      if user_claps is not None:
        user_num_claps = user_claps.num_claps
      else:
        user_num_claps = 0
      return(jsonify(total=total_num_claps, user=user_num_claps), 200)
  return ('', 400)


# creates a pageview record, and a page if it does not yet exist
@bp.route('/view', methods=['POST'])
@cross_origin()
def view():
  # Create a page view record
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
