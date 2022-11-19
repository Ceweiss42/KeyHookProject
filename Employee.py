from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
from Request import Requests


class Employees(Base):
    __tablename__ = "employees"
    employee_id = Column('employee_id', Integer, Identity(start=1, cycle=True),
                        nullable=False, primary_key=True)
    first_name = Column('first_name', String(50), nullable=False)
    last_name = Column('last_name', String(50), nullable=False)

    # Employee does not have a candidate key.
    # Employee does not have a candidate key
    # Employee is one of the parents in a many to many relationship.
    # Many to Many relationship with Student Requests
    #requests_list: [Requests] = relationship("Requests", back_populates="employee", viewonly=False)

    requests = relationship("Requests", back_populates="employees")

    #Constructor
    def __init__(self, first_name: String, last_name: String):
        self.first_name = first_name
        self.last_name = last_name
        self.requests_list = []

    """Add an employee to the list of requests that apply to this employee.
        @param request The instance of request tied to this employee."""

    def add_request(self, request):
        # make sure this request is non already on the list.
        for next_request in self.requests_list:
            if next_request == request:
                #message stating that the request has already made
                print("Request already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        employee_request = Requests(self, request)
        # Update this move to reflect that we have this request.
        request.employee_list.append(employee_request)
        # Update the genre to reflect this request.
        self.requests_list.append(employee_request)

