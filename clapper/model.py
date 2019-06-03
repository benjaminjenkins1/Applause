from clapper import db

class User(db.Model):
  __tablename__ = 'users'

  email = db.Column(db.String(), primary_key=True)
  pass_hash = db.Column(db.String())

  def __init__(self, email, pass_hash):
    self.email = email
    self.pass_hash = pass_hash

  def __repr__(self):
    return '<email {}>'.format(self.email)
