from flask import Flask

from .config import app_config
from .models import db

from .views.EmployeeView import employee_api as employee_blueprint


def create_app(env_name):
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  app.config.from_object(app_config[env_name])

  db.init_app(app)

  app.register_blueprint(employee_blueprint, url_prefix='/api/v1/company')

  @app.route('/', methods=['GET'])
  def index():
    """
    example endpoint
    """
    return 'Congratulations! Your first endpoint is workin'

  return app