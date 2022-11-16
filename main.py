"""HookKey Project Phase Two:  Using SQL Alchemy to create an application for key requests"""


from pprint import pprint
from sqlalchemy import Column, String, Integer, Float, UniqueConstraint, \
    Identity, ForeignKey, distinct, bindparam
from sqlalchemy.orm import relationship, backref
from Building import Building
from Employee import Employee
from DoorName import DoorName
from Hook import Hook
from Door import Door
from HookDoor import HookDoor
from Key import Key
from KeyIssuance import KeyIssuance
from LossKey import LossKey
#from Request import Request
from ReturnKey import ReturnKey
from Room import Room
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

    #create variables for tables that will be populated manually.
    # variables to populate the building Table
    building1: Building("Engineering")
    building2: Building("Psychology")
    building3: Building("Science")
    building4: Building("Metal Shop")
    building5: Building("Lecture Hall")

    # variables to populate the employee table
    employee1: Employee("Ed", "Aguilar")
    employee2: Employee("Cam", "Weiss")
    employee3: Employee("Jim", "Ha")
    employee4: Employee("Jeff", "Lucena")

    # variables to populate the DoorName table
    doorname1: DoorName("North")
    doorname2: DoorName("South")
    doorname3: DoorName("East")
    doorname4: DoorName("West")
    doorname5: DoorName("Front")
    doorname6: DoorName("Back")

    # Do our database work within a context.  This makes sure that the session gets closed
    # at the end of the with, much like what it would be like if you used a with to open a file.
    # This way, we do not have memory leaks.
    with Session() as sess:
        sess.begin()
        print("Inside the session, woo hoo.")
        # add the buildings
        sess.add(building1)
        sess.add(building2)
        sess.add(building3)
        sess.add(building4)
        sess.add(building5)
        # add the employees
        sess.add(employee1)
        sess.add(employee2)
        sess.add(employee3)
        sess.add(employee4)
        # add the doorNames
        sess.add(doorname1)
        sess.add(doorname2)
        sess.add(doorname3)
        #sec3.add_student(s1)
        #sec3.add_student(s2)
        #sec3.add_student(s3)
        #sess.commit()

print("Exiting normally.")