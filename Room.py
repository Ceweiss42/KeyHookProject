from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKeyConstraint, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.orm import relationship
from Building import Building

from orm_base import Base
from Building import Building


class Room(Base):
    __tablename__ = "rooms"
    room_number = Column('room_number', Integer, nullable=False, primary_key=True)
    building_name = Column('building_name', String(40), ForeignKey('buildings.building_name'),
                           nullable=False, primary_key=True)
    #ForeignKeyConstraint([building_name], ['buildings.building_name'], name="fk_rooms_building_01")

    # One to many relationship between building and room
    # NOTE: the r_building naming convention caused an error.  removing it allowed the relationship to form properly. EA
    building = relationship("Buildings", back_populates="rooms")
    doors = relationship("Doors", back_populates="rooms")
    requests = relationship("Requests", back_populates="rooms")

 #   door = relationship("Door", back_populates="room")

    # Many to Many relationship

    #constructor
    def __init__(self, room_number: Integer, building):
        self.room_number = room_number
        self.building_name = building.building_name


# request_list: [Request] = relationship("Request", back_populates="room", viewonly=False)
""" # One to many relationship between room and door
    r_door = relationship("Door", back_populates="room", viewonly=False)
    #
    r_request = relationship('Request', back_populates='room')
    # candidate key
    table_args = (UniqueConstraint('room_number', 'building_name', name='room_uk_01'),)



"""

"""
    def add_request(self, request):
        # make sure this request is non already on the list.
        for next_request in self.request_list:
            if next_request == request:
                # message stating that the request has already made
                print("Request already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        room_request = Request(employee, self)
        # Update this move to reflect that we have this request.
        employee.add_request(room_request)
        # Update the genre to reflect this request.
        self.request_list.append(room_request)

"""
