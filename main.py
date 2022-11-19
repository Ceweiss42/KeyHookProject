"""HookKey Project Phase Two:  Using SQL Alchemy to create an application for key requests"""

from pprint import pprint
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint, \
    Identity, ForeignKey, distinct, bindparam
from sqlalchemy.orm import relationship, backref
from Building import Building
from Room import Room
from DoorName import DoorName
from Door import Door
from Request import Requests
from Hook import Hooks
from HookDoor import HookDoors
from Key import Keys
from Employee import Employees
#from KeyIssuance import KeyIssuances

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
        building1: Building = Building("Bob Murphy Access Center")
        sess.add(building1)
        dn1: DoorName = DoorName("East")
        sess.add(dn1)


        '''building2: Building = Building("Hall of Science")
        building3: Building = Building("Vivian Engineering Center")
        building4: Building = Building("Engineering and Computer Science")
        building5: Building = Building("Horn Center")
        building6: Building = Building("Engineering Technologies")
        # create a room variable
        room1: Room = Room(100, building1)
        room2: Room = Room(101, building2)
        room3: Room = Room(100, building5)
        room4: Room = Room(107, building6)
        room5: Room = Room(419, building3)
        room6: Room = Room(124, building4)
        room7: Room = Room(518, building3)
        # create a door name variable
        doorName1: DoorName = DoorName("North")
        doorName2: DoorName = DoorName("West")
        doorName3: DoorName = DoorName("South")
        doorName4: DoorName = DoorName("East")
        doorName5: DoorName = DoorName("Front")
        doorName6: DoorName = DoorName("Back")
        # create a door
        door1: Door = Door(doorName1, room1)
        door2: Door = Door(doorName2, room2)
        door3: Door = Door(doorName3, room3)
        door4: Door = Door(doorName2, room4)
        door5: Door = Door(doorName1, room5)
        door6: Door = Door(doorName3, room6)
        door7: Door = Door(doorName5, room7)
        door8: Door = Door(doorName1, room6)
        door9: Door = Door(doorName6, room2)
        # create a hook
        hook1: Hooks = Hooks()
        hook2: Hooks = Hooks()
        hook3: Hooks = Hooks()
        hook4: Hooks = Hooks()
        hook5: Hooks = Hooks()
        hook6: Hooks = Hooks()
        hook7: Hooks = Hooks()
        hook8: Hooks = Hooks()

        #create hookDoors!
        hookDoor1: HookDoors = HookDoors(hook1, door1)
        hookDoor2: HookDoors = HookDoors(hook2, door2)
        hookDoor3: HookDoors = HookDoors(hook3, door5)
        hookDoor4: HookDoors = HookDoors(hook4, door7)
        hookDoor5: HookDoors = HookDoors(hook5, door1)
        hookDoor6: HookDoors = HookDoors(hook6, door9)
        hookDoor7: HookDoors = HookDoors(hook7, door5)
        hookDoor8: HookDoors = HookDoors(hook8, door4)
        hookDoor9: HookDoors = HookDoors(hook1, door6)
        hookDoor10: HookDoors = HookDoors(hook4, door3)
        hookDoor11: HookDoors = HookDoors(hook2, door2)
        hookDoor12: HookDoors = HookDoors(hook8, door1)
        hookDoor13: HookDoors = HookDoors(hook6, door8)

        #add employees
        employee1: Employees = Employees("Cameron", "Weiss")
        employee2: Employees = Employees("Ed", "Aguilar")
        employee3: Employees = Employees("Jimmy", "Something")
        employee4: Employees = Employees("Jeff", "Something")
        employee5: Employees = Employees("David", "Brown")

        #create keys!
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


        #add employees
        sess.add(employee1)
        sess.add(employee2)
        sess.add(employee3)
        sess.add(employee4)
        sess.add(employee5)


        # add buildings
        sess.add(building1)
        sess.add(building2)
        sess.add(building3)
        sess.add(building4)
        sess.add(building5)
        sess.add(building6)
        # add rooms
        sess.add(room1)
        sess.add(room2)
        sess.add(room3)
        sess.add(room4)
        sess.add(room5)
        sess.add(room6)
        sess.add(room7)
        # add doorNames
        sess.add(doorName1)
        sess.add(doorName2)
        sess.add(doorName3)
        sess.add(doorName4)
        sess.add(doorName5)
        sess.add(doorName6)
        #add a door
        sess.add(door1)
        sess.add(door2)
        sess.add(door3)
        sess.add(door4)
        sess.add(door5)
        sess.add(door6)
        sess.add(door7)
        sess.add(door8)
        sess.add(door9)
        #add a hook
        sess.add(hook1)
        sess.add(hook2)
        sess.add(hook3)
        sess.add(hook4)
        sess.add(hook5)
        sess.add(hook6)
        sess.add(hook7)
        sess.add(hook8)

        #add hookDoors
        sess.add(hookDoor1)
        sess.add(hookDoor2)
        sess.add(hookDoor3)
        sess.add(hookDoor4)
        sess.add(hookDoor5)
        sess.add(hookDoor6)
        sess.add(hookDoor7)
        sess.add(hookDoor8)
        sess.add(hookDoor9)
        sess.add(hookDoor10)
        sess.add(hookDoor11)
        sess.add(hookDoor12)
        sess.add(hookDoor13)

        #add keys
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
        sess.add(key13)'''

        sess.commit()

print("Exiting normally.")
