"""HookKey Project Phase Two:  Using SQL Alchemy to create an application for key requests"""
import datetime
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
#import logging




def viewTable(tableNum, session):
    tables = [Buildings, Rooms, DoorNames, Doors, Employees, HookDoors, Hooks, Keys, LossKeys, Requests, ReturnKeys]
    search = session.query(tables[tableNum])
    for row in search:
        print(row)

def runCreateRequest(userID, session):
    print("Here are all of the rooms:")
    rooms = session.query(Rooms)
    i = 0
    for room in rooms:
        print(i , ". " , room)
        i += 1

    chosenRoom = None
    try:
        choice = int(input("What room would you like access to?(Enter Room Row)"))
        if choice < 0 or choice > i:
            print("Please enter a valid room")
            runCreateRequest(userID, session)
        else:
            chosenRoom = rooms[choice]
            print(chosenRoom)
            haveAccess = session.query(Requests).filter(chosenRoom.room_number == Requests.room_number and
                                                        chosenRoom.building_name == Requests.building_name and
                                                        userID == Requests.employee_id)
            count = 0
            for row in haveAccess:
                count += 1

            if count == 0:
                #they don't have access
                emp = session.query(Employees).filter(userID == Employees.employee_id)[0]
                #now we need the key
                hookdoor = session.query(HookDoors).filter(chosenRoom.room_number == HookDoors.room_number and
                                                   chosenRoom.building_name == HookDoors.building_name)[0]
                key = session.query(Keys).filter(Keys.key_number == hookdoor.hook_number)[0]


                newReq: Requests = Requests(emp, chosenRoom, key)
                session.add(newReq)
                session.commit()
                print("\n\nYou have created this request:")
                print(newReq)
                print("\n\nSuccessfully submitted a Request\n\n\n")

            else:
                #check the return list to see if they've returned it
                for req in haveAccess:
                    returned = session.query(ReturnKeys).filter(ReturnKeys.request_request_id == req.request_id)
                    c = 0
                    for r in returned:
                        c += 1
                    if c == 0:
                        #you have not returned it
                        print("You already have acess to this room!")
                        return

                emp = session.query(Employees).filter(userID == Employees.employee_id)[0]
                # now we need the key
                hookdoor = session.query(HookDoors).filter(chosenRoom.room_number == HookDoors.room_number and
                                                           chosenRoom.building_name == HookDoors.building_name)[0]
                key = session.query(Keys).filter(Keys.key_number == hookdoor.hook_number)[0]

                newReq: Requests = Requests(emp, chosenRoom, key)
                session.add(newReq)
                session.commit()
                print("\n\nYou have created this request:")
                print(newReq)
                print("\n\nSuccessfully submitted a Request\n\n\n")





    except ValueError:
        print("Please a valid Room")
        runCreateRequest(userID, session)

def addDoor(session):
    print("Here are all of the door names:")
    doornames = session.query(DoorNames)
    i = 0
    for dn in doornames:
        print(i, ". ", dn)
        i += 1

    try:
        choice = int(input("Enter the index of a door name!"))
        if choice > i or choice < 0:
            print("Invalid input, try again")
            addDoor(session)
        else:
            print("What room should this door be fore?")
            rooms = session.query(Rooms)
            c = 0
            for r in rooms:
                print(c, ". ", r)
                c += 1
            try:
                roomChoice = int(input("Please enter the index of the room:"))
                if roomChoice > c or roomChoice < 0:
                    print("invalid input, please try again")
                    addDoor(session)
                else:
                    newDoor: Doors = Doors(doornames[dn], rooms[roomChoice])
                    session.add(newDoor)
                    session.commit()
            except ValueError:
                print("invalid input, please try again")
                addDoor(session)

    except ValueError:
        print("invalid input, please try again")
        addDoor(session)


def runRequestOptions(user, session):
    print("What would you like to do?")
    print("0. Request a Key\n1. Return a Key\n2. Report a Lost Key")

    try:
        option = int(input())
        if option < 0 or option > 2:
            print("Please enter a valid option")
            runRequestOptions(user, session)
        else:
            #we have input a correct option
            if option == 0:
                runCreateRequest(user, session)
            elif option == 1:
                #Ask for the request ID
                try:

                    print("Here are all the requests you currently have\n")
                    request_ids = session.query(Requests).filter(Requests.employee_id == user)
                    shrunk_requests: [Requests] = []
                    for row in request_ids:
                        returned = session.query(ReturnKeys).filter(ReturnKeys.request_request_id == row.request_id)
                        lost = session.query(LossKeys).filter(LossKeys.request_request_id == row.request_id)
                        c = 0
                        for _ in returned:
                            c += 1

                        for _ in lost:
                            c += 1

                        if c == 0:
                            #that request has NOT been returned
                            shrunk_requests.append(row)

                    i = 0
                    for req in shrunk_requests:
                        print(i, ". ", req)
                        i += 1

                    if i == 0:
                        print("You currently have no requests that have not been returned")
                        return
                    loc = int(input("Enter the request index\n"))
                    if loc < 0 or loc > i:
                        print("You entered an invalid index")
                        runRequestOptions(user, session)
                    else:
                        selected_req = shrunk_requests[loc]
                        #######################################
                        returnedRequest: ReturnKeys = ReturnKeys(selected_req, selected_req.requested_date)
                        #grab the date
                        '''print("Here are all the dates that the key was loaned out\n")
                        loaned_dates = session.query(Requests)
                        i = 0
                        for loaned_date in loaned_dates:
                            print(i, ". ", loaned_date)
                            i += 1
    
                        returned_loaned_date = int(input("Enter the date you were loaned the key out\n"))
                        res1 = session.query(ReturnKeys).filter(ReturnKeys.loaned_date == returned_loaned_date)[0]
                        #####################################
                        returned_date = input("Please enter the date you are returning the key\n")
                        res3 = session.query(ReturnKeys).filter(ReturnKeys.return_date == returned_date)[0]
    
                        new_returned_key: ReturnKeys = ReturnKeys(res1,res2,res3)'''
                        session.add(returnedRequest)
                        session.commit()
                        print("You successfully closed the request (returned)")

                    #print our request ID?
                except ValueError:
                    print("Error: entered wrong value")
                    runRequestOptions(user, session)

            else:
                print("Here are all the requests you currently have\n")
                request_ids = session.query(Requests).filter(Requests.employee_id == user)
                shrunk_requests: [Requests] = []
                for row in request_ids:
                    returned = session.query(ReturnKeys).filter(ReturnKeys.request_request_id == row.request_id)
                    lost = session.query(LossKeys).filter(LossKeys.request_request_id == row.request_id)
                    c = 0
                    for _ in returned:
                        c += 1

                    for _ in lost:
                        c += 1

                    if c == 0:
                        # that request has NOT been returned OR lost
                        shrunk_requests.append(row)

                i = 0
                for req in shrunk_requests:
                    print(i, ". ", req)
                    i += 1

                if i == 0:
                    print("You currently have no requests that have not been returned/lost")
                    return
                loc = int(input("Enter the request index\n"))
                if loc < 0 or loc > i:
                    print("You entered an invalid index")
                    runRequestOptions(user, session)
                else:
                    lostRequest: LossKeys = LossKeys(shrunk_requests[loc], shrunk_requests[loc].requested_date)
                    session.add(lostRequest)
                    session.commit()
                    print("You successfully closed the request (lost)")






    except ValueError:
        print("Please enter a valid option")
        runRequestOptions(user, session)
def runViewSystem(session):
    printViewMenu()
    try:
        choice = int(input())
        if choice < 0 or choice > 10:
            print("Please enter a number within the range")
            runViewSystem(session)
        else:
            viewTable(choice, session)

    except ValueError:
        print("Error, you have typed in a wrong error, please try again")
        runViewSystem(session)

    # give the computer our employee id
    # take that id, and spit all requests that this id made
    # send back our request choice
    # asks what to do(return, loss)
    # create a new instance of return/loss of that request
def runRequestSystem(session):
    try:
        user_id = int(input("Please enter your ID\n"))

        res = session.query(Employees).filter(Employees.employee_id == user_id)
        count = 0
        for row in res:
            count += 1
        if count == 0:
            print("Please enter a valid ID")
            runRequestSystem(session)
        else:
            print("Welcome, " + res[0].first_name + " " + res[0].last_name)
            runRequestOptions(user_id, session)





    except ValueError:
        print("Please enter a valid id")
        runRequestSystem(session)

def getAccessibleRooms(session):
    try:
        user_id = int(input("Please enter your ID\n"))

        res = session.query(Employees).filter(Employees.employee_id == user_id)
        count = 0
        for row in res:
            count += 1
        if count == 0:
            print("Please enter a valid ID")
            getAccessibleRooms(session)
        else:
            print("Welcome, " + res[0].first_name + " " + res[0].last_name)
            print("You have access to the following rooms:")
            myReqs = session.query(Requests).filter(res[0].employee_id == Requests.employee_id)
            shrunkReqs: [Requests] = []
            for r in myReqs:
                returned = session.query(ReturnKeys).filter(ReturnKeys.request_request_id == r.request_id)
                lost = session.query(LossKeys).filter(LossKeys.request_request_id == r.request_id)
                c = 0
                for _ in returned:
                    c += 1

                for _ in lost:
                    c += 1

                if c == 0:
                    shrunkReqs.append(r)

            roomsList: [Rooms] = []
            for r in shrunkReqs:
                room = session.query(Rooms).filter(Rooms.room_number == r.room_number and Rooms.building_name == r.building_name)
                roomsList.append(room)

            for room in roomsList:
                print(room)

    except ValueError:
        print("Please enter a valid id")
        getAccessibleRooms(session)

def deleteEmployee(session):
    print("Here all all the employees")
    emps = session.query(Employees)
    i = 0
    for e in emps:
        i += 1
        print(e)

    print("Please enter an employee id:\n")
    try:
        choice = int(input())
        if choice < 0 or choice > i:
            print("You entered an incorrect value")
            deleteEmployee(session)
        else:
            session.query(Employees).filter(Employees.employee_id == choice).delete()
            session.commit()
            print("Deleted the selected Employee")
    except ValueError:
        print("You entered an incorrect value")
        deleteEmployee(session)


def deleteKey(session):
    print("here are all the keys")
    keys = session.query(Keys)
    i = 0
    for k in keys:
        i += 1
        print(k)

    print("Please enter the id of the key you would like to delete:")
    try:
        choice = int(input())
        if choice < 0 or choice > i:
            print("You entered an incorrect value")
            deleteKey(session)
        else:
            session.query(Keys).filter(Keys.key_id == choice).delete()
            session.commit()
            print("Deleted the selected key")
    except ValueError:
        print("You entered an incorrect value")
        deleteKey(session)


def printMainMenu():
    print("What would you like to do?")
    print("0. View")
    print("1. Manage Requests")
    print("2. View Rooms You Have Access to")
    print("3. Delete a Key")
    print("4. Delete Employee")
    print("5. Add Door")
    print("6. Update Request to new Employee")
    print("7. Exit\n")

def printViewMenu():
    print("You have chosen to view the tables")
    print("What table would you like to view? Available tables are:")
    print("0. buildings\n1. rooms\n2. door_names\n3. doors\n4. employees\n5. hook_doors"
          "\n6. hooks\n7. keys\n8. loss_keys\n9. requests\n10. return_keys")


if __name__ == '__main__':

    #the console output from sqlalchemy got annoying, so we removed logging and the echo on engine

    #logging.basicConfig()
    # use the logging factory to create our first logger.
    #logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    # use the logging factory to create our second logger.
    #logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

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

        req1: Requests = Requests(employee1, room6, key5)
        req2: Requests = Requests(employee5, room5, key3)
        req3: Requests = Requests(employee3, room2, key1)
        req4: Requests = Requests(employee2, room1, key1)
        req5: Requests = Requests(employee3, room4, key4)
        req6: Requests = Requests(employee4, room3, key2)
        sess.add(req1)
        sess.add(req2)
        sess.add(req3)
        sess.add(req4)
        sess.add(req5)
        sess.add(req6)
        sess.commit()
        # add lostkey
        losskey1: LossKeys = LossKeys(req1, datetime.datetime(2022, 11, 15))
        losskey2: LossKeys = LossKeys(req4, datetime.datetime(2020, 3, 21))
        losskey3: LossKeys = LossKeys(req3, datetime.datetime(2021, 7, 11))
        losskey4: LossKeys = LossKeys(req2, datetime.datetime(2019, 7, 5))
        losskey5: LossKeys = LossKeys(req1, datetime.datetime(2022, 2, 7))
        losskey6: LossKeys = LossKeys(req1, datetime.datetime(2022, 9, 10))
        losskey7: LossKeys = LossKeys(req6, datetime.datetime(2022, 11, 30))
        sess.add(losskey1)
        sess.add(losskey2)
        sess.add(losskey3)
        sess.add(losskey4)
        sess.add(losskey5)
        sess.add(losskey6)
        sess.add(losskey7)
        sess.commit()

        ret1: ReturnKeys = ReturnKeys(req1, datetime.datetime(2022, 11, 10))
        ret2: ReturnKeys = ReturnKeys(req4, datetime.datetime(2022, 3, 21))
        ret3: ReturnKeys = ReturnKeys(req3, datetime.datetime(2021, 7, 6))
        ret4: ReturnKeys = ReturnKeys(req2, datetime.datetime(2001, 9, 14))
        ret5: ReturnKeys = ReturnKeys(req1, datetime.datetime(2022, 8, 13))
        ret6: ReturnKeys = ReturnKeys(req1, datetime.datetime(2022, 9, 10))
        ret7: ReturnKeys = ReturnKeys(req6, datetime.datetime(2022, 11, 13))
        sess.add(ret1)
        sess.add(ret2)
        sess.add(ret3)
        sess.add(ret4)
        sess.add(ret5)
        sess.add(ret6)
        sess.add(ret7)
        sess.commit()

    #searchResult = sess.query(Rooms)
    #for row in searchResult:
    #    print(row)

    it_is = False
    while not it_is:
        try:
            printMainMenu()
            choice = int(input())
            if (choice >= 0) and (choice <= 7):
                it_is = True
            else:
                print("invalid range, please enter a value between 0 and 2")
                it_is = False
        except ValueError:
            print("invalid input, please enter a correct value.")
            it_is = False

    #now we have a valid input, lets check:
        if choice == 7:
            print("Exiting the program! Goodbye...")
            exit()
        it_is = False

        with Session() as sess:
            if choice == 0:
                runViewSystem(sess)

            elif choice == 1:
                runRequestSystem(sess)

            elif choice == 2:
                getAccessibleRooms(sess)
            elif choice == 3:
                deleteKey(sess)

            elif choice == 4:
                deleteEmployee(sess)





    # ok, user has chosen

    # start application console stuff



# this is the update
