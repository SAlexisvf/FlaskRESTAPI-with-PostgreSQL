from flask_sqlalchemy import SQLAlchemy

# initialize our db
db = SQLAlchemy()

from .ProjectModel import ProjectModel, ProjectSchema
from .EmployeeModel import EmployeeModel, EmployeeSchema