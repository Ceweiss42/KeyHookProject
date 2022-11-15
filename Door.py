from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from Hook import Hook
from HookDoor import HookDoor

from orm_base import Base

from DoorName import DoorName
from Room import Room


class Door(Base):
    __tablename__ = "doors"
    door_name = Column('door_name', String(20), ForeignKey('door_names.door_name'),
                       nullable=False, primary_key=True)
    room_number = Column('room_number', Integer, ForeignKey('rooms.room_number'),
                         nullable=False, primary_key=True)
    building_name = Column('building_name', String(40), ForeignKey('buildings.building_name'),
                           nullable=False, primary_key=True)

    # Building does not have a candidate key
    # One-to-many relationship between DoorName and Door
    door_name = relationship("Door", back_populates="doors", viewonly=False)
    # One-to-many relationship between Room and Door
    rooms_doors = relationship("Door", back_populates="room", viewonly=False)
    rooms_building_name_doors = relationship("Door", back_populates="building_name", viewonly=False)
    # Many-to-many relationship with Hook
    hook_list: [HookDoor] = relationship("HookDoor", back_populates="door", viewonly=False)

    # Constructor
    def __init__(self, door_name: DoorName, room_reference: Room):
        self.door_name = door_name.door_name
        self.room_number = room_reference.room_number
        self.building_name = room_reference.building_name
        self.hook_list = []

    """Add an door to the list of hooks.
        @param door The instance of door tied to this hook."""

    def add_hook(self, hook):
        # make sure this request is non already on the list.
        for next_hook in self.hook_list:
            if next_hook == hook:
                # message stating that the request has already made
                print("Hook already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        hook_door = HookDoor(hook, self)
        # Update this move to reflect that we have this request.
        hook.add_door(self)
        # Update the genre to reflect this request.
        self.hook_list.append(hook_door)