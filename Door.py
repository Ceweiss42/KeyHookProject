from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from orm_base import Base
from DoorName import DoorNames
from Room import Rooms
from HookDoor import HookDoors


class Doors(Base):
    __tablename__ = "doors"
    door_name = Column('door_name', String(20), ForeignKey('door_names.door_name'),
                       nullable=False, primary_key=True)
    room_number = Column('room_number', Integer,  #ForeignKey('rooms.room_number'),
                         nullable=False, primary_key=True)
    building_name = Column('building_name', String(40),  # ForeignKey('rooms.building_name'),
                           nullable=False, primary_key=True)
    # Foreign Key Constraint for Rooms because it has more than one column coming from rooms
    __table_args__ = (ForeignKeyConstraint(['room_number', 'building_name'], ['rooms.room_number', 'rooms.building_name'],
                         name="fk_doors_rooms_01"),)

    # One-to-many relationship between DoorName and Door
    doornames = relationship("DoorNames", back_populates="doors", viewonly=False)
    # One-to-many relationship between Room and Door
    rooms = relationship("Rooms", back_populates="doors", viewonly=False)

    hooks_list: [HookDoors] = relationship("HookDoors", back_populates="doors", viewonly=False)

    # Constructor
    def __init__(self, door_name, room):
        self.door_name = door_name.door_name
        self.room_number = room.room_number
        self.building_name = room.building_name
        self.hooks_list = []

    def __str__(self):
        return str("Door Name: "+ str(self.door_name) +"     Room Number: " + str(self.room_number) +
                   "     Building Name: " + str(self.building_name))

    def add_hook(self, hook):
        # make sure this request is non already on the list.
        for next_hook in self.hooks_list:
            if next_hook == hook:
                # message stating that the request has already made
                print("Hook already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        hook_door = HookDoors(hook, self)
        # Update this move to reflect that we have this request.
        hook.add_door(hook_door)
        # Update the genre to reflect this request.
        self.hooks_list.append(hook_door)

