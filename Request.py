from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from orm_base import Base

class Requests(Base):
    __tablename__ = "requests"

    room_number = Column('room_number', Integer, nullable=False, primary_key=False)
    building_name = Column('building_name', String(40), nullable=False, primary_key=False)
    employee_id = Column('employee_id', Integer, nullable=False, primary_key=False)
    requested_date = Column('requested_date', DateTime(timezone=False), default=func.now(), nullable=False, primary_key=False)
    key_number = Column('key_number', Integer, nullable=False, primary_key=False)
    key_id = Column('key_id', Integer, nullable=False, primary_key=False)
    request_id = Column('request_id', Integer, Identity(start=1, cycle=True), nullable=False, primary_key=True)

    __table_args__ = (ForeignKeyConstraint(['room_number', 'building_name'], ['rooms.room_number', 'rooms.building_name']),
                      ForeignKeyConstraint(['employee_id'], ['employees.employee_id']),
                      ForeignKeyConstraint(['key_number', 'key_id'], ['keys.key_number', 'keys.key_id']),)

    #key_issuance = relationship("KeyIssuance", back_populates='request', viewonly=False)
    employees = relationship('Employees', back_populates='requests', viewonly=False)
    rooms = relationship('Rooms', back_populates='requests', viewonly=False)
    keys = relationship("Keys", back_populates="requests")
    returnkeys = relationship("ReturnKeys", back_populates="requests")
    losskeys = relationship("LossKeys", back_populates="requests")



    def __init__(self, employee, room, key):
        self.room_number = room.room_number
        self.building_name = room.building_name
        self.employee_id = employee.employee_id
        self.key_number = key.key_number
        self.key_id = key.key_id
        self.key_issuances_list = []

    def add_key_issuance(self, key_issuance):
        for next_ki in self.key_issuances_list:
            if next_ki == key_issuance:
                print("THIS REQUEST HAS ALREADY BEEN FILLED")
                return

        #key_issuance =


    