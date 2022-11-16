from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from orm_base import Base
from Request import Requests
from Employee import Employees


class Rooms(Base):
    __tablename__ = "rooms"
    room_number = Column("room_number", Integer, nullable=False, primary_key=True)
    building_name = Column('building_name', String(40), ForeignKey('buildings.building_name'),
                           nullable=False, primary_key=True)
    #One to many relationship between building and room
    r_building = relationship("Building", back_populates="room", viewonly=False)
    #One to many relationship between room and door
    r_door = relationship("Door", back_populates="room", viewonly=False)

    # Building does not have a candidate key
    # Many to Many relationship
    request_list: [Requests] = relationship("Request", back_populates="room", viewonly=False)

    def __init__(self, room_number: Integer, building_name: String(40)):
        self.room_number = room_number
        self.building_name = building_name
        self.request_list = []

    def add_request(self, request: Requests, employee: Employees):
        # make sure this request is non already on the list.
        for next_request in self.request_list:
            if next_request == request:
                # message stating that the request has already made
                print("Request already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        room_request = Requests(employee, self)
        # Update this move to reflect that we have this request.
        employee.add_request(room_request)
        # Update the genre to reflect this request.
        self.request_list.append(room_request)



