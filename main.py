"""HookKey Project Phase Two:  Using SQL Alchemy to create an application for key requests"""

from pprint import pprint
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint, \
    Identity, ForeignKey, distinct, bindparam
from sqlalchemy.orm import relationship, backref
from Building import Building
from Room import Room
from DoorName import DoorName
from Door import Door
from Hook import Hooks

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
        print("Inside the session, woo hoo.")

        # create a building variable
        building1: Building = Building("Science")
        building2: Building = Building("Engineering")
        # create a room variable
        room1: Room = Room(100, building1)
        room2: Room = Room(101, building1)
        # create a door name variable
        doorName1: DoorName = DoorName("North")
        doorName2: DoorName = DoorName("West")
        doorName3: DoorName = DoorName("South")
        doorName4: DoorName = DoorName("East")
        # create a door
        door1: Door = Door(doorName1, room1)
        door2: Door = Door(doorName2, room1)
        # create a hook
        hook1: Hooks = Hooks(1)

        # add buildings
        sess.add(building1)
        sess.add(building2)
        # add rooms
        sess.add(room1)
        sess.add(room2)
        # add doorNames
        sess.add(doorName1)
        sess.add(doorName2)
        sess.add(doorName3)
        sess.add(doorName4)
        #add a door
        sess.add(door1)
        #add a hook
        sess.add(hook1)

        sess.commit()

print("Exiting normally.")
