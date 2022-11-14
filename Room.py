from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from orm_base import Base
from Room import Room


class Room(Base):
    __tablename__ = "rooms"
    room_number = Column("room_number", Integer, nullable=False, primary_key=True)
    building_name = Column('building_name', String(40), ForeignKey('buildings.building_name'),
                           nullable=False, primary_key=True)
    #One to many relationship between building and room
    building = relationship("Building", back_populates="Room")

    # Building does not have a candidate key
    # One to many relationship for Building and Rooms

    def __init__(self, room_reference: Room):
        self.room_number = room_number
        self.building_name = building.building_name
