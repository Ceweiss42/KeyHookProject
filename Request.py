from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, TimeStamp
from sqlalchemy.orm import relationship

from Hook import Hook
from DoorName import DoorName
from Request import Request
from KeyIssuances import KeyIssuances

from orm_base import Base

class Request(Base):
    __tablename__ = "requests"
    room_number = Column('room_number', Integer, ForeignKey('rooms.room_number'), nullable=False, primary_key=False)
    building_name = Column('building_name', String(40), ForeignKey('rooms.building_name'), nullable=False, primary_key=False)
    employee_id = Column('employee_id', Integer, ForeignKey('employees.employee_id'), nullable=False, primary_key=False)
    requested_date = Column('requested_date', TimeStamp, nullable=False, primary_key=False)
    key_number = Column('key_number', Integer, ForeignKey('keys.key_number'), nullable=False, primary_key=False)
    request_id = Column('request_id', Integer, nullable=False, primary_key=True)

    key_issuances_list : [KeyIssuances] = relationship("KeyIssuance", back_populates='request', view_only=False)

    r_employee_id = relationship ('EmployeeID', back_populates='requests', viewonly=False)

    def __init__(self, roomNum : Integer, bName : String(40), empID : Integer, reqDate : TimeStamp, kNum : Integer, request_id : Integer):
        self.room_number = roomNum
        self.building_name = bName
        self.employee_id = empID
        self.requested_date = reqDate
        self.key_number = kNum
        self.request_id = request_id
        self.key_issuances_list = []

    def add_key_issuance(self):
        print("THIS IS A TEST")
        pass


    