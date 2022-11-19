from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from orm_base import Base


class HookDoors(Base):
    __tablename__ = "hook_doors"
    door_name = Column('door_name', String(20), #ForeignKey('doors.door_name'),
                        nullable=False, primary_key=True)
    room_number = Column('room_number', Integer,# ForeignKey('rooms.room_number'),
                        nullable=False, primary_key=True)
    building_name = Column('building_name', String(40), nullable=False, primary_key=True)

    hook_number = Column('hook_number', Integer, ForeignKey('hooks.hook_number'), nullable=False, primary_key=True)

    __table_args__ = (ForeignKeyConstraint(['door_name', 'room_number', 'building_name'], ['doors.door_name', 'doors.room_number', 'doors.building_name'],
                         name="fk_hook_doors_rooms_01"),)
    #ForeignKeyConstraint(['door_name'], ['doors.door_name'], name='fk_hook_doors_doors_01')


    """This is a bi-directional relationship between Hook and Door."""
    hooks = relationship("Hooks", back_populates='doors_list')
    # movies_list is the name of the list of MovieGenre instances for the parent movie.
    doors = relationship("Doors", back_populates='hooks_list')

    # Hookdoor does not have a candidate key

    # Constructor
    def __init__(self, hook, door):
        self.hook = hook.hook_number
        self.door = door.door_name

        # These next two properties are strictly from the OO perspective.
        self.door = door
        self.hook = hook
