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

    # create students
    s1: Student = Student(last_name="Aguilar", first_name="Ed")
    s2: Student = Student(last_name="Weiss", first_name="Cam")
    s3: Student = Student(last_name="Somebody", first_name="Joe")

    # create sections
    sec1: Section = Section(department_name="CECS", course_name="Database Fun", section_number=1,
                            semester="Fall", year=2022)
    sec2: Section = Section(department_name="CECS", course_name="Database Fun", section_number=2,
                            semester="Fall", year=2022)
    sec3: Section = Section(department_name="CECS", course_name="Database Fun", section_number=3,
                            semester="Fall", year=2022)


    # Do our database work within a context.  This makes sure that the session gets closed
    # at the end of the with, much like what it would be like if you used a with to open a file.
    # This way, we do not have memory leaks.
    with Session() as sess:
        sess.begin()
        print("Inside the session, woo hoo.")
        # add the students
        sess.add(s1)
        sess.add(s2)
        sess.add(s3)
        # add the sections
        sess.add(sec1)
        sess.add(sec2)
        sess.add(sec3)
        # insert into sections_students.
        sec3.add_student(s1)
        sec3.add_student(s2)
        sec3.add_student(s3)
        sess.commit()

    print("Exiting normally.")
