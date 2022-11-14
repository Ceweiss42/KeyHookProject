from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
from Room import Room

class Building(Base):
    __tablename__ = "buildings"
    building_name = Column('building_name', String(40), nullable=False, primary_key=True)

    # Building does not have a candidate key
    # One to many relationship for Building and Rooms
    # Building.rooms = relationship("Room", back_populates="building_name", viewonly=False)

    def __init__(self, building_name: String(40)):
        self.building_name = building_name
