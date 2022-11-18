from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from orm_base import Base


class DoorName(Base):
    __tablename__ = "door_names"
    door_name = Column('door_name', String(20), nullable=False, primary_key=True)

    # DoorName does not have a candidate key
    # DoorName is not a child to a relationship.
    door = relationship("Door", back_populates="doorname", viewonly=False)

    # Constructor for instance of DoorName
    def __init__(self, door_name: String):
        self.door_name = door_name
