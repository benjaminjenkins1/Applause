from applause import db


class User(db.Model):
  __tablename__ = 'users'

  email = db.Column(db.String(), primary_key=True)
  pass_hash = db.Column(db.String(), nullable=False)
  activated = db.Column(db.Boolean(), default=False, nullable=False)
  banned = db.Column(db.Boolean, default=False, nullable=False)

  domains = db.relationship('Domain', backref='user', lazy=True)
  keys = db.relationship('Key', backref='user', lazy=True)

  def __repr__(self):
    return '<email {}>'.format(self.email)


class Domain(db.Model):
  __tablename__ = 'domains'
  __table_args__ = (
    db.UniqueConstraint('domain_name', 'email', name='unique_email_and_domain'),
  )

  did = db.Column(db.Integer, primary_key=True)
  domain_name = db.Column(db.String(), nullable=False)
  email = db.Column(db.String(), db.ForeignKey('users.email'), nullable=False)

  pages = db.relationship('Page', backref='domain', lazy=True)

  def __repr__(self):
    return '<did {}>'.format(self.did)


class Key(db.Model):
  __tablename__ = 'keys'

  uuid = db.Column(db.String(), primary_key=True)
  did = db.Column(db.Integer, db.ForeignKey('domains.did'), nullable=False)
  email = db.Column(db.String(), db.ForeignKey('users.email'), nullable=False)

  def __repr__(self):
    return '<uuid {}>'.format(self.uuid)


class Page(db.Model):
  __tablename__ = 'pages'
  __table_args__ = (
    db.UniqueConstraint('did', 'path', name='unique_path_and_did'),
  )

  pid = db.Column(db.Integer, primary_key=True)
  did = db.Column(db.Integer, db.ForeignKey('domains.did'), nullable=False)
  path = db.Column(db.String(), nullable=False)
  total_claps = db.Column(db.Integer, default=0, nullable=False)

  claps = db.relationship('Clap', backref='page', lazy=True)

  def __repr__(self):
    return '<pid {}>'.format(self.pid)


class Clap(db.Model):
  __tablename__ = 'claps'
  
  pid = db.Column(db.Integer, db.ForeignKey('pages.pid'), primary_key=True)
  ip = db.Column(db.String(), primary_key=True)
  num_claps = db.Column(db.Integer, default=0, nullable=False)

  def __repr__(self):
    return '<pid {} ip {}>'.format(self.pid, self.ip)
