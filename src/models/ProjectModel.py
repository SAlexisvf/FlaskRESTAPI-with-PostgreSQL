from . import db
import datetime
from marshmallow import fields, Schema

class ProjectModel(db.Model):
  """
  Project Model
  """

  __tablename__ = 'projects'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(128), nullable=False)
  description = db.Column(db.Text, nullable=False)
  owner_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  def __init__(self, data):
    self.title = data.get('title')
    self.description = data.get('description')
    self.owner_id = data.get('owner_id')
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
    de.session.commit()
  
  @staticmethod
  def get_all_projects():
    return ProjectModel.query.all()
  
  @staticmethod
  def get_one_project(id):
    return ProjectModel.query.get(id)

  def __repr__(self):
    return '<id {}>'.format(self.id)

class ProjectSchema(Schema):
  """
  Project Schema
  """
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  description = fields.Str(required=True)
  owner_id = fields.Int(required=True)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)