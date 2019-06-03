import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SQLALCHEMY_TRACK_MODIFICATIONS=False
  )

  if test_config is None:
    # Load the instance config
    app.config.from_pyfile('config.cfg')
  else:
    # Load the test config
    app.config.from_mapping(test_config)

  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  from clapper.model import (
    User,
    Domain,
    Key,
    Page,
    Clap
  )

  # Route that just says 'Hello!'
  @app.route('/hello')
  def hello():
    return 'Hello!'

  db.init_app(app)
  migrate.init_app(app, db)

  return app
