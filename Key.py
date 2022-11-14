from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from Hook import Hook
from DoorName import DoorName
from Request import Request

from orm_base import Base


class Key(Base):
    __tablename__ = "keys"
    key_number = Column('key_number', Integer, ForeignKey('hooks.hook_number'), nullable=False, primary_key=True)

    # Key does not have a candidate key
    # One to many relationship between hook and key
    hook_key = relationship("Key", back_populates="key_number", viewonly=False)
    # Key is a parent to a many to many relationship between Key and Requests
    # Many to many relationship with requests
    requests_list: [Request] = relationship("Request", back_populates="key", viewonly=False)

    # Constructor
    def __init__(self, key_number: Integer):
        self.key_number = key_number
        self.requests_list = []

    """Add an employee to the list of requests that apply to this employee.
            @param request The instance of request tied to this key."""

    def add_request(self, request):
        # make sure this request is non already on the list.
        for next_request in self.requests_list:
            if next_request == request:
                # message stating that the request has already made
                print("Request already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        key_request = Request(self, request)
        # Update this move to reflect that we have this request.
        request.key_list.append(key_request)
        # Update the genre to reflect this request.
        self.requests_list.append(key_request)

