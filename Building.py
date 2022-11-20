from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
#from Room import Room

class Buildings(Base):
    __tablename__ = "buildings"
    building_name = Column('building_name', String(40), nullable=False, primary_key=True)
    #relationship between building to room
    rooms = relationship("Rooms", back_populates="buildings")


    def __init__(self, building_name: String(40)):
        self.building_name = building_name

    def __str__(self):
        return str("Building Name: " + str(self.building_name) )