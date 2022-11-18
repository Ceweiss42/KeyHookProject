from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
#from Room import Room

class Building(Base):
    __tablename__ = "buildings"
    building_name = Column('building_name', String(40), nullable=False, primary_key=True)
    #relationship between building to room
    # NOTE: the r_building naming convention caused an error.  removing it allowed the relationship to form properly. EA
    room = relationship("Room", back_populates="building")
    # Building does not have a candidate key


    def __init__(self, building_name: String(40)):
        self.building_name = building_name
