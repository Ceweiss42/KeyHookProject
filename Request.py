from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from KeyIssuance import KeyIssuance
from orm_base import Base


class Request(Base):
    __tablename__ = "requests"
    room_number = Column('room_number', Integer, ForeignKey('rooms.room_number'), nullable=False)
    building_name = Column('building_name', String(40), ForeignKey('rooms.building_name'), nullable=False)
    employee_id = Column('employee_id', Integer, ForeignKey('employees.employee_id'), nullable=False, primary_key=False)
    requested_date = Column('requested_date', DateTime, nullable=False, primary_key=False)
    key_number = Column('key_number', Integer, ForeignKey('keys.key_number'), nullable=False, primary_key=False)
    request_id = Column('request_id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)
    #Many to Many relationship with KeyIssuance
    key_issuances_list: [KeyIssuance] = relationship("KeyIssuance", back_populates='request')
    #one to many relationships with Employee, Key and Room
    r_employee = relationship('Employee', back_populates='request', viewonly=False)
    r_key = relationship('Key', back_populates='request', viewonly=False)
    r_room = relationship('Room', back_populates='request')

    def __init__(self, employee, room, key, reqDate: DateTime):
        self.room_number = room.room_number
        self.building_name = room.building_name
        self.employee_id = employee.employee_id
        self.requested_date = reqDate
        self.key_number = key.key_number
        self.key_issuances_list = []

    def add_key_issuance(self, key_issuance):
        for next_ki in self.key_issuances_list:
            if next_ki == key_issuance:
                print("THIS REQUEST HAS ALREADY BEEN FILLED")
                return

        # key_issuance =
