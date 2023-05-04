import logging
logger = logging.getLogger(__name__)

from sqlalchemy import func
from sqlalchemy.schema import CheckConstraint
from marshmallow import fields, Schema
from faker import Faker
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

SQLDB = SQLAlchemy()

# Employee Model
class EmployeeModel(SQLDB.Model):
    '''
    Employee Model
    '''
    __tablename__ = 'employee'
    __versioned__ = {}

    id = SQLDB.Column(SQLDB.Integer, primary_key=True, autoincrement=True)
    name = SQLDB.Column(SQLDB.String(50), nullable=False)
    department = SQLDB.Column(SQLDB.String(50), nullable=False)
    salary = SQLDB.Column(SQLDB.Integer, nullable=False)
    hire_date = SQLDB.Column(SQLDB.DateTime, nullable=False, default=datetime.utcnow, index=True, server_default=func.now(),)

    # defining the constaint for hire_date
    hire_date_constraint = CheckConstraint('hire_date >= "2020-01-01 00:00:00" AND hire_date <= NOW()', name='check_hire_date')
    SQLDB.Index('ix_employee_hire_date', 'hire_date')
    __table_args__ = (hire_date_constraint, {})

    # class constructor
    def __init__(self, data):
        '''
        Class constructor
        '''
        self.name = data.get('name')
        self.department = data.get('department')
        self.salary = data.get('salary')
        self.hire_date = data.get('hire_date')

    def save(self):
        '''
        Save to database
        '''
        SQLDB.session.add(self)
        SQLDB.session.commit()

    def delete(self):
        SQLDB.session.delete(self)
        SQLDB.session.commit()

    @staticmethod
    def get_all_employees():
        '''
        Get all employees
        '''
        return EmployeeModel.query.all()
    
    @staticmethod
    def get_one_employee(id):
        '''
        Get one employee
        '''
        return EmployeeModel.query.get(id)
    
    @staticmethod
    def get_employee_by_name(name):
        '''
        Get employee by name
        '''
        return EmployeeModel.query.filter_by(name=name).first()
    
    @staticmethod
    def get_employee_by_department(department):
        '''
        Get employee by department
        '''
        return EmployeeModel.query.filter_by(department=department).first()
    
    # return a list of all unique departments
    @staticmethod
    def get_all_departments():
        '''
        Get all departments
        '''
        return EmployeeModel.query.with_entities(EmployeeModel.department).distinct().all()
    
    # Returns the average salary of employees in the specified department.
    @staticmethod
    def get_average_salary_by_department(department):
        '''
        Get average salary by department
        '''
        return EmployeeModel.query.with_entities(func.avg(EmployeeModel.salary)).filter_by(department=department).first()
    
    # Returns a list of the top 10 earners in the company based on their salary
    @staticmethod
    def get_top_10_earners():
        '''
        Get top 10 earners
        '''
        return EmployeeModel.query.order_by(EmployeeModel.salary.desc()).limit(10).all()
    
    # Returns a list of the 10 new employees in the company (sorted by hire date)
    @staticmethod
    def get_last_10_hired():
        '''
        Get last 10 hired
        '''
        return EmployeeModel.query.order_by(EmployeeModel.hire_date.desc()).limit(10).all()
    

# Generate fake data
fake = Faker()

def generate_fake_data():
    '''
    Generate fake data
    '''
    for _ in range(1000):
        employee = EmployeeModel(
            name=fake.name(),
            department=fake.job(),
            salary=fake.random_int(min=0, max=1000000),
            hire_date=fake.date_between(start_date='01-01-2020 00:00:00', end_date='today')
        )
        employee.save()

    
# Create a database
def create_db():
    '''
    Create a database
    '''
    SQLDB.create_all()
    SQLDB.session.commit()
