from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from Hook import Hooks
from HookDoor import HookDoors

from orm_base import Base

from DoorName import DoorNames
from Room import Rooms


class Doors(Base):
    __tablename__ = "doors"
    # ForeignKey('door_names.door_name'),
    door_name = Column('door_name', String(20),
                       nullable=False, primary_key=True)
    # ForeignKey('rooms.room_number'),
    room_number = Column('room_number', Integer,
                         nullable=False, primary_key=True)
    #ForeignKey('rooms.building_name'),
    building_name = Column('building_name', String(40),
                           nullable=False, primary_key=True)


#UniqueConstraint('building_name', 'room_number', 'door_name', name='door_uk_01'),
    __table_args__ = (
                      ForeignKeyConstraint(['room_number', 'building_name'], ['rooms.room_number', 'rooms.building_name']),
                      ForeignKeyConstraint(['door_name'], ['door_names.door_name']),)

    # Building does not have a candidate key
    # One-to-many relationship between DoorName and Door
    r_door_name = relationship("DoorName", back_populates="door", viewonly=False)
    # One-to-many relationship between Room and Door
    rooms_doors = relationship("Room", back_populates="door", viewonly=False)
    rooms_building_name_doors = relationship("Room", back_populates="door", viewonly=False)
    # Many-to-many relationship with Hook
    hook_list: [HookDoors] = relationship("HookDoor", back_populates="door", viewonly=False)

    # Constructor
    def __init__(self, door_name: DoorNames, room_reference: Rooms):
        self.door_name = door_name.door_name
        self.room_number = room_reference.room_number
        self.building_name = room_reference.building_name
        self.hook_list = []

    """Add an door to the list of hooks.
        @param door The instance of door tied to this hook."""

    #testing

    def add_hook(self, hook: Hooks):
        # make sure this request is non already on the list.
        for next_hook in self.hook_list:
            if next_hook == hook:
                # message stating that the request has already made
                print("Hook already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        hook_door = HookDoors(hook, self)
        # Update this move to reflect that we have this request.
        hook.add_door(hook_door)
        # Update the genre to reflect this request.
        self.hook_list.append(hook_door)
