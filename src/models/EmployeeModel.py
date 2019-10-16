from marshmallow import fields, Schema
import datetime
from . import db
from .ProjectModel import ProjectSchema

class EmployeeModel(db.Model):
  """
  Employee Model
  """

  # table name
  __tablename__ = 'employees'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  position = db.Column(db.String(128), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  projects = db.relationship('ProjectModel', backref='employees', lazy=True)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.email = data.get('email')
    self.position = data.get('position')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def get_all_employees():
    return EmployeeModel.query.all()

  @staticmethod
  def get_one_employee(id):
    return EmployeeModel.query.get(id)

  @staticmethod
  def get_employee_by_email(value):
    return EmployeeModel.query.filter_by(email=value).first()

  
  def __repr(self):
    return '<id {}>'.format(self.id)

class EmployeeSchema(Schema):
  """
  Employee Schema
  """
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  position = fields.Str(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  projects = fields.Nested(ProjectSchema, many=True)