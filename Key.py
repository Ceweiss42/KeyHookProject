from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from Request import Requests

from orm_base import Base


class Keys(Base):
    __tablename__ = "keys"
    key_number = Column('key_number', Integer, ForeignKey('hooks.hook_number'), #nullable=False,
                        primary_key=True)
    key_id = Column('key_id', Integer, Identity("key_id_seq", start=1),
                         nullable=False, primary_key=True)

    # Key does not have a candidate key
    # One to many relationship between hook and key
    hooks = relationship("Hooks", back_populates="keys")
    # Key is a parent to a many to many relationship between Key and Requests
    # Many to many relationship with requests
    #requests_list: [Requests] = relationship("Requests", back_populates="keys", viewonly=False)
    requests = relationship("Requests", back_populates="keys")


    # Constructor
    def __init__(self, original_hook):
        self.key_number = original_hook.hook_number
        self.requests_list = []

    def __str__(self):
        return str("Key Number: " + str(self.key_number) + "     Key ID: " + str(self.key_id)) #might just be key_id

    """Add an employee to the list of requests that apply to this employee.
            @param request The instance of request tied to this key."""

    def add_request(self, request):
        # make sure this request is non already on the list.
        for next_request in self.requests_list:
            if next_request == request:
                # message stating that the request has already made
                print("Request already exist.")
                return
        # Update the genre to reflect this request.
        self.requests_list.append(request)

