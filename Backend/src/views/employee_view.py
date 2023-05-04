import logging
logger = logging.getLogger(__name__)
import io
from flask import Flask, request, g, Blueprint, Response, json
from src.models.employee_model import EmployeeModel
muvid_api = Blueprint('muvid_api', __name__)

# API Endpoints
@muvid_api.route('/employees', methods=['GET'])
def get_all_employees():
    '''
    Get all employees
    '''
    employees = EmployeeModel.get_all_employees()
    return Response(
        response=json.dumps(employees),
        status=200,
        mimetype='application/json'
    )
