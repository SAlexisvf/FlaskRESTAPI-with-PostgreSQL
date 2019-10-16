from flask import request, json, Response, Blueprint
from ..models.EmployeeModel import EmployeeModel, EmployeeSchema

employee_api = Blueprint('employees', __name__)
employee_schema = EmployeeSchema()

@employee_api.route('/employee', methods=['POST'])
def createEmployee():
  """
  Create Employee Function
  """
  req_data = request.get_json()
  data = employee_schema.load(req_data)
  
  # check if employee already exist in the db
  employee_in_db = EmployeeModel.get_employee_by_email(data.get('email'))
  if employee_in_db:
    message = {'error': 'Employee email already exist, please provide another email address'}
    return custom_response(message, 400)
  
  employee = EmployeeModel(data)
  employee.save()

  parsed_data = employee_schema.dump(employee)

  return custom_response({'created': parsed_data}, 201)
  
@employee_api.route('/employees', methods=['GET'])
def get_all_employees():
  employees = EmployeeModel.get_all_employees()
  parsed_employees = employee_schema.dump(employees, many=True)
  return custom_response(parsed_employees, 200)

@employee_api.route('employee/<int:employee_id>', methods=['GET'])
def get_a_employee(employee_id):
  """
  Get a single employee
  """
  employee = EmployeeModel.get_one_employee(employee_id)
  if not employee:
    return custom_response({'error': 'employee not found'}, 404)
  
  parsed_employee = employee_schema.dump(employee)
  return custom_response(parsed_employee, 200)

@employee_api.route('employee/<int:employee_id>', methods=['DELETE'])
def delete(employee_id):
  """
  Delete an employee
  """
  employee = EmployeeModel.get_one_employee(employee_id)
  employee.delete()
  return custom_response({'deleted': 'True'}, 204)

@employee_api.route('employee/<int:employee_id>', methods=['PUT'])
def update(employee_id):
  """
  Update and employee
  """
  req_data = request.get_json()
  data = employee_schema.load(req_data, partial=True)

  employee = EmployeeModel.get_one_employee(employee_id)
  employee.update(data)
  parsed_employee = employee_schema.dump(employee)
  return custom_response(parsed_employee, 200)

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )