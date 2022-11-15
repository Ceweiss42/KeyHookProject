from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from orm_base import Base
from Hook import Hook
from Door import Door


class HookDoor(Base):
    __tablename__ = "hook_doors"
    door_name = Column('door_name', String(20), ForeignKey('doors.door_name'), nullable=False, primary_key=True)
    room_number = Column('room_number', Integer, ForeignKey('rooms.room_number'), nullable=False, primary_key=True)
    building_name = Column('building_name', String(40), ForeignKey('doors.building_name'), nullable=False,
                           primary_key=True)
    hook_number = Column('hook_number', Integer, ForeignKey('hooks.hook_number'), nullable=False, primary_key=True)

    """This is a bi-directional relationship between Hook and Door."""
    hook = relationship("Hook", back_populates='door_list')
    # movies_list is the name of the list of MovieGenre instances for the parent movie.
    door = relationship("Door", back_populates='hook_list')

    # Hookdoor does not have a candidate key

    # Constructor
    def __init__(self, hook: Hook, door: Door):
        self.hook = hook.hook_number
        self.door = door.door_name

        # These next two properties are strictly from the OO perspective.
        self.door = door
        self.hook = hook
