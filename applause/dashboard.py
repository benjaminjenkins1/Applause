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

from applause import db

from applause.auth import login_required

from applause.model import (
  Domain,
  Key,
  Page,
  PageView,
  Clap
)

from applause.forms import (
  AddDomainForm,
  AddKeyForm,
  DeleteKeyForm
)

from sqlalchemy import func

import uuid

def get_domain_summary(domain):
  total_views = len(db.session.query(PageView, Page).filter(Page.did == domain.did, PageView.pid == Page.pid).all())
  all_claps = db.session.query(Clap, Page).filter(Page.did == domain.did, Clap.pid == Page.pid).all()
  total_claps = 0
  for clap in all_claps:
    total_claps += clap[0].num_claps
  return {
    'views': total_views,
    'claps': total_claps
  }

def get_pages_data(domain):
  page_data = []
  all_pages = domain.pages.all()
  for page in all_pages:
    this_page = { 'path': page.path, 
                  'views': 0,
                  'claps': 0 }
    # add views for this page
    this_page['views'] = len(PageView.query.filter_by(pid=page.pid).all())
    # add claps for this page
    all_page_claps = db.session.query(Clap, Page).filter(Page.did == domain.did, Clap.pid == page.pid).all()
    for clap in all_page_claps:
      this_page['claps'] += clap[0].num_claps
    page_data.append(this_page)
  return page_data

def get_referrers_data(domain):
  referrers_data = {}
  
  return referrers_data

bp = Blueprint('dashboard', __name__, url_prefix='/my')

@bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
  domains = Domain.query.filter_by(email=g.user.email).order_by(Domain.did).all()
  return render_template('dashboard/dashboard.html', domains=domains)

@bp.route('/add_domain', methods=['GET','POST'])
@login_required
def add_domain():
  form = AddDomainForm()
  if form.is_submitted() and form.validate_on_submit():
    domain_name = form.domain_name.data
    exists = Domain.query.filter_by(email=g.user.email, domain_name=domain_name).first() is not None
    if not exists:
      new_domain = Domain(domain_name=domain_name, email=g.user.email)
      db.session.add(new_domain)
      db.session.commit()
      return redirect(url_for('dashboard.dashboard'))
    else:
      flash('You have already added this domain')
  return render_template('dashboard/add_domain.html', form=form)

@bp.route('/domain_detail', methods=['GET'])
@login_required
def domain_detail():
  if request.args.get('did') is None:
    return redirect(url_for('dashboard.dashboard'))
  did = request.args.get('did')
  domain = Domain.query.filter_by(email=g.user.email, did=did).first()
  if domain is None:
    return redirect(url_for('dashboard.dashboard'))
  keys = domain.keys
  #skipping time for now
  #time = request.args.get('time')
  summary = get_domain_summary(domain)
  pages = get_pages_data(domain)
  referrers = get_referrers_data(domain)
  add_key_form = AddKeyForm()
  delete_key_form = DeleteKeyForm()
  return render_template('dashboard/domain_detail.html', 
                         domain=domain, 
                         keys=keys, 
                         add_key_form=add_key_form, 
                         delete_key_form=delete_key_form,
                         summary=summary,
                         pages=pages,
                         #time = time
                         )

@bp.route('/add_key', methods=['POST'])
@login_required
def add_key():
  form = AddKeyForm()
  if form.is_submitted() and form.validate_on_submit():
    did = form.did.data
    user_email = g.user.email
    # add a new key to the database for this user on this domain
    # generate a uuid
    key_uuid = uuid.uuid4()
    # add the key to the db
    new_key = Key(uuid=key_uuid, did=did, email=g.user.email)
    db.session.add(new_key)
    db.session.commit()
    return redirect(url_for('dashboard.domain_detail', did=did))
  flash('There was a problem adding a new key for this domain')
  return redirect(url_for('dashboard.dashboard'))

@bp.route('/delete_key', methods=['POST'])
@login_required
def delete_key():
  form = DeleteKeyForm()
  if form.is_submitted() and form.validate_on_submit():
    uuid = form.uuid.data
    did = form.did.data
    # remove the key with this uuid and email of the user from the database
    Key.query.filter(Key.uuid==uuid, Key.email==g.user.email).delete()
    db.session.commit()
    return redirect(url_for('dashboard.domain_detail', did=did))
  flash('There was a problem removing the key for this domain')
  return redirect(url_for('dashboard.dashboard'))
