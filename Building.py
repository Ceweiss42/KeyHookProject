from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
from Room import Rooms

class Buildings(Base):
    __tablename__ = "buildings"
    building_name = Column('building_name', String(40), nullable=False, primary_key=True)
    #relationship between building to room
    r_room = relationship("Room", back_populates="buildings", viewonly=False)
    # Building does not have a candidate key


    def __init__(self, building_name: String(40)):
        self.building_name = building_name
