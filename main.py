"""HookKey Project Phase Two:  Using SQL Alchemy to create an application for key requests"""

from pprint import pprint
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint, \
    Identity, ForeignKey, distinct, bindparam
from sqlalchemy.orm import relationship, backref
from Building import Buildings
from Room import Rooms
from DoorName import DoorNames
from Door import Doors
from Request import Requests
from Hook import Hooks
from HookDoor import HookDoors
from Key import Keys
from Employee import Employees
from ReturnKey import ReturnKeys
from LossKey import LossKeys

import sqlalchemy.sql.functions
from db_connection import Session, engine
from orm_base import metadata
import logging

if __name__ == '__main__':
    logging.basicConfig()
    # use the logging factory to create our first logger.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    # use the logging factory to create our second logger.
    logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.  The simple fact that
    # your classes that are subtypes of Base have been loaded by Python has populated
    # the metadata object with their definition.  So now we tell SQLAlchemy to create
    # those tables for us.
    metadata.create_all(bind=engine)

    # Do our database work within a context.  This makes sure that the session gets closed
    # at the end of the with, much like what it would be like if you used a with to open a file.
    # This way, we do not have memory leaks.
    with Session() as sess:
        sess.begin()
        print("Inside the session...")

        # create a building variable

        building1: Buildings = Buildings("Bob Murphy Acess Center")
        building2: Buildings = Buildings("Hall of Science")
        building3: Buildings = Buildings("Vivian Engineering Center")
        building4: Buildings = Buildings("Engineering and Computer Science")
        building5: Buildings = Buildings("Horn Center")
        building6: Buildings = Buildings("Engineering Technologies")
        sess.add(building1)
        sess.add(building2)
        sess.add(building3)
        sess.add(building4)
        sess.add(building5)
        sess.add(building6)
        sess.commit()

        # create a room variable
        room1: Rooms = Rooms(100, building1)
        room2: Rooms = Rooms(101, building2)
        room3: Rooms = Rooms(100, building5)
        room4: Rooms = Rooms(107, building6)
        room5: Rooms = Rooms(419, building3)
        room6: Rooms = Rooms(124, building4)
        room7: Rooms = Rooms(518, building3)
        sess.add(room1)
        sess.add(room2)
        sess.add(room3)
        sess.add(room4)
        sess.add(room5)
        sess.add(room6)
        sess.add(room7)
        sess.commit()
        # create a door name variable
        doorName1: DoorNames = DoorNames("North")
        doorName2: DoorNames = DoorNames("West")
        doorName3: DoorNames = DoorNames("South")
        doorName4: DoorNames = DoorNames("East")
        doorName5: DoorNames = DoorNames("Front")
        doorName6: DoorNames = DoorNames("Back")
        sess.add(doorName1)
        sess.add(doorName2)
        sess.add(doorName3)
        sess.add(doorName4)
        sess.add(doorName5)
        sess.add(doorName6)
        sess.commit()
        # create a door
        door1: Doors = Doors(doorName1, room1)
        door2: Doors = Doors(doorName2, room2)
        door3: Doors = Doors(doorName3, room3)
        door4: Doors = Doors(doorName2, room4)
        door5: Doors = Doors(doorName1, room5)
        door6: Doors = Doors(doorName3, room6)
        door7: Doors = Doors(doorName5, room7)
        door8: Doors = Doors(doorName1, room6)
        door9: Doors = Doors(doorName6, room2)
        sess.add(door1)
        sess.add(door2)
        sess.add(door3)
        sess.add(door4)
        sess.add(door5)
        sess.add(door6)
        sess.add(door7)
        sess.add(door8)
        sess.add(door9)
        sess.commit()
        # create a hook
        hook1: Hooks = Hooks()
        hook2: Hooks = Hooks()
        hook3: Hooks = Hooks()
        hook4: Hooks = Hooks()
        hook5: Hooks = Hooks()
        hook6: Hooks = Hooks()
        hook7: Hooks = Hooks()
        hook8: Hooks = Hooks()
        sess.add(hook1)
        sess.add(hook2)
        sess.add(hook3)
        sess.add(hook4)
        sess.add(hook5)
        sess.add(hook6)
        sess.add(hook7)
        sess.add(hook8)
        sess.commit()

        key1: Keys = Keys(hook2)
        key2: Keys = Keys(hook1)
        key3: Keys = Keys(hook5)
        key4: Keys = Keys(hook2)
        key5: Keys = Keys(hook6)
        key6: Keys = Keys(hook8)
        key7: Keys = Keys(hook7)
        key8: Keys = Keys(hook2)
        key9: Keys = Keys(hook3)
        key10: Keys = Keys(hook1)
        key11: Keys = Keys(hook2)
        key12: Keys = Keys(hook7)
        key13: Keys = Keys(hook4)
        sess.add(key1)
        sess.add(key2)
        sess.add(key3)
        sess.add(key4)
        sess.add(key5)
        sess.add(key6)
        sess.add(key7)
        sess.add(key8)
        sess.add(key9)
        sess.add(key10)
        sess.add(key11)
        sess.add(key12)
        sess.add(key13)
        sess.commit()

        # create hookDoors!
        hook1.add_door(door1)
        hook1.add_door(door2)
        hook2.add_door(door3)
        hook2.add_door(door4)
        hook3.add_door(door9)
        hook4.add_door(door4)
        hook5.add_door(door5)
        hook6.add_door(door6)
        hook7.add_door(door7)
        hook8.add_door(door8)

        sess.commit()

        # add employees
        employee1: Employees = Employees("Cameron", "Weiss")
        employee2: Employees = Employees("Ed", "Aguilar")
        employee3: Employees = Employees("Jimmy", "Something")
        employee4: Employees = Employees("Jeff", "Something")
        employee5: Employees = Employees("David", "Brown")
        sess.add(employee1)
        sess.add(employee2)
        sess.add(employee3)
        sess.add(employee4)
        sess.add(employee5)

        sess.commit()

print("Exiting normally.")
