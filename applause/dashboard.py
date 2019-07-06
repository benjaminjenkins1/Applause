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
  Key
)

from applause.forms import (
  AddDomainForm
)

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
    print(domain_name)
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
  if request.args.get('domain') is None:
    return redirect(url_for('dashboard.dashboard'))
  domain_name = request.args.get('domain')
  domain = Domain.query.filter_by(email=g.user.email, domain_name=domain_name).first()
  if domain is None:
    return redirect(url_for('dashboard.dashboard'))
  keys = Domain.query.filter_by(domain_name=domain.domain_name, email=g.user.email).join(Domain.keys).all()
  return render_template('dashboard/domain_detail.html', domain=domain, keys=keys)
