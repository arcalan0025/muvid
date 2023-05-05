import logging
from sqlalchemy import func, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from faker import Faker
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M:%S")

# Set up the database
engine = create_engine('sqlite:///employees.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Employee Model
class EmployeeModel(Base):
    '''
    Employee Model
    '''
    __tablename__ = 'employee'
    __versioned__ = {}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    salary = Column(Integer, nullable=False)
    hire_date = Column(DateTime, nullable=False, default=datetime.utcnow, index=True, server_default=func.now())

    # class constructor
  # class constructor
    def __init__(self, name, department, salary, hire_date):
        '''
        Class constructor
        '''
        self.name = name
        self.department = department
        self.salary = salary
        self.hire_date = hire_date


    def save(self):
        '''
        Save to database
        '''
        session = Session()
        session.add(self)
        session.commit()

    def delete(self):
        session = Session()
        session.delete(self)
        session.commit()

    @staticmethod
    def get_all_employees():
        '''
        Get list all employees
        '''
        session = Session()
        return session.query(EmployeeModel).all()

    @staticmethod
    def get_one_employee(id):
        '''
        Get one employee
        '''
        session = Session()
        return session.query(EmployeeModel).get(id)

    # return a list of all unique departments
    @staticmethod
    def get_all_departments():
        '''
        Get all departments
        '''
        session = Session()
        return session.query(EmployeeModel.department).distinct().all()
    
    @staticmethod
    def get_department_by_name(department):
        '''
        Search for department by department name
        '''
        session = Session()
        return session.query(EmployeeModel).filter_by(department=department).all()

    # Returns the average salary of employees in the specified department.
    @staticmethod
    def get_average_salary_by_department(department):
        '''
        Get average salary by department
        '''
        session = Session()
        average_salary = session.query(func.avg(EmployeeModel.salary)).filter_by(department=department).scalar()
        average_salary = round(average_salary, 2)
        return average_salary

    # Returns a list of the top 10 earners in the company based on their salary
    @staticmethod
    def get_top_10_earners():
        '''
        Get top 10 earners
        '''
        session = Session()
        top_10_earners = session.query(EmployeeModel).order_by(EmployeeModel.salary.desc()).limit(10).all()
        earners_list = []
        for employee in top_10_earners:
            employee_dict = {
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'salary': employee.salary,
                'hire_date': employee.hire_date.strftime('%Y-%m-%d')
                }
            earners_list.append(employee_dict)
        
        return earners_list

    # Returns a list of the 10 new employees in the company (sorted by hire date)
    @staticmethod
    def get_last_10_hired():
        '''
        Get last 10 hired
        '''
        session = Session()
        latest_hires = session.query(EmployeeModel).order_by(EmployeeModel.hire_date.desc()).limit(10).all()
        latest_hires_dict = []

        for employee in latest_hires:
            employee_dict = {
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'salary': employee.salary,
                'hire_date': employee.hire_date.strftime('%Y-%m-%d')
            }
            latest_hires_dict.append(employee_dict)

        return latest_hires_dict


    # Returns a name list of all employees in the specified department.
    @staticmethod
    def get_employees_by_department(department):
        '''
        Get the list of names of all employees in the specified department
        '''
        session = Session()
        results = session.query(EmployeeModel.name).filter_by(department=department).all()
        employees = [dict(row) for row in results]
        return employees

    @staticmethod
    def delete_employee(id):
        '''
        Delete employee
        '''
        session = Session()
        session.query(EmployeeModel).filter_by(id=id).delete()
        session.commit()

# Generate fake data
fake = Faker()

def generate_fake_data():
    '''
    Generate fake data
    '''
    session = Session()
    existing_records = session.query(EmployeeModel).count()
    if existing_records > 0:
        return "Fake data already generated. Skipping data generation."
    
    for _ in range(1000):
        employee = EmployeeModel(
            name=fake.name(),
            department=fake.job(),
            salary=fake.random_int(min=0, max=1000000),
            hire_date=fake.date_between(start_date='01-01-2020', end_date='today')
        )
        employee.save()


Base.metadata.create_all(engine)
generate_fake_data()
