"""This "application" is a demonstration using SQLAlchemy to create a small number of tables and populate
them.  Not evey possible use case for SQLAlchemy is explored in this demonstration, only those which are
required for this particular demonstration.

Technical Note: Be sure to have psycopg2 or whichever package you need to support whichever
relational dialect that you are using installed.  No imports call attention to the database
connectivity library, that is referenced when you run your application."""

# Think of Session and engine like global variables.  A little ghetto, but the only
# other alternative would have been a singleton design pattern.
from pprint import pprint

import sqlalchemy.sql.functions

# the db_connection.py code sets up some connection objects for us, almost like Java class variables
# that get loaded up at run time.  This statement builds the Session class and the engine object
# that we will use for interacting with the database.
from db_connection import Session, engine
# orm_base defines the Base class on which we build all of our Python classes and in so doing,
# stipulates that the schema that we're using is 'demo'.  Once that's established, any class
# that uses Base as its supertype will show up in the postgres.demo schema.
from orm_base import metadata
import logging
from DoorName import DoorNames
from Door import Doors
from Room import Rooms
from Building import Buildings
from Employee import Employees

from sqlalchemy import Column, String, Integer, Float, UniqueConstraint, \
    Identity, ForeignKey, distinct, bindparam
from sqlalchemy.orm import relationship, backref
from orm_base import Base


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

    """
    southDoorName: DoorName = DoorName("South")
    northDoorName: DoorName = DoorName("North")
    VEC: Building = Building("VEC")
    standardRoom: Room = Room(419, VEC)
    standardDoorA: Door = Door(southDoorName, standardRoom"""

    # populate the building Table
    building1: Buildings("Engineering")
    building2: Buildings("Psychology")
    building3: Buildings("Science")
    building4: Buildings("Metal Shop")
    building5: Buildings("Lecture Hall")

    # populate the employee table
    employee1: Employees("Ed", "Aguilar")
    employee2: Employees("Cam", "Weiss")
    employee3: Employees("Jim", "Ha")
    employee4: Employees("Jeff", "Lucena")

    # populate the DoorName table
    doorname1: DoorNames("North")
    doorname2: DoorNames("South")
    doorname3: DoorNames("East")
    doorname4: DoorNames("West")
    doorname5: DoorNames("Front")
    doorname6: DoorNames("Back")


    # Do our database work within a context.  This makes sure that the session gets closed
    # at the end of the with, much like what it would be like if you used a with to open a file.
    # This way, we do not have memory leaks.
    with Session() as sess:
        sess.begin()
        print("Inside the session, woo hoo.")






    print("Exiting normally.")
