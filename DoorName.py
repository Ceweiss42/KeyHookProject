from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from orm_base import Base


class DoorNames(Base):
    __tablename__ = "door_names"
    door_name = Column('door_name', String(20), nullable=False, primary_key=True)

    # DoorName does not have a candidate key
    # DoorName is not a child to a relationship.
    doors = relationship("Doors", back_populates="doornames", viewonly=False)

    # Constructor for instance of DoorName
    def __init__(self, door_name: String):
        self.door_name = door_name
    def __str__(self):
        return str("Door Name: "+ str(self.door_name))