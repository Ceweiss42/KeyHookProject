from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship


from KeyIssuance import KeyIssuances

from orm_base import Base

class Requests(Base):
    __tablename__ = "requests"

    room_number = Column('room_number', Integer, ForeignKey('rooms.room_number'), nullable=False, primary_key=False)
    building_name = Column('building_name', String(40), ForeignKey('rooms.building_name'), nullable=False, primary_key=False)
    employee_id = Column('employee_id', Integer, ForeignKey('employees.employee_id'), nullable=False, primary_key=False)
    requested_date = Column('requested_date', DateTime, nullable=False, primary_key=False)
    key_number = Column('key_number', Integer, ForeignKey('keys.key_number'), nullable=False, primary_key=False)
    request_id = Column('request_id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)

    r_key_issuance = relationship("KeyIssuance", back_populates='request', viewonly=False)
    r_employee = relationship('Employee', back_populates='requests_list', viewonly=False)
    r_key = relationship('Key', back_populates='requests_list', viewonly=False)
    r_room = relationship('Room', back_populates='request_list', viewonly=False)



    def __init__(self, employee, room, key, reqDate):
        self.room_number = room.room_number
        self.building_name = room.building_name
        self.employee_id = employee.employee_id
        self.requested_date = reqDate
        self.key_number = key.key_number
        self.key_issuances_list = []

    def add_key_issuance(self, key_issuance : KeyIssuances):
        for next_ki in self.key_issuances_list:
            if next_ki == key_issuance:
                print("THIS REQUEST HAS ALREADY BEEN FILLED")
                return

        #key_issuance =


    