import os

from flask import (
  Flask,
  render_template,
  g,
  redirect,
  url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

name='applause'

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

  # Route that just says 'Hello!'
  @app.route('/')
  def index():
    if g.user is not None:
      return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')

  db.init_app(app)
  migrate.init_app(app, db)

  with app.app_context():

    from . import auth
    app.register_blueprint(auth.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    from . import analytics
    app.register_blueprint(analytics.bp)

    return app
