from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from orm_base import Base


class ReturnKeys(Base):
    __tablename__ = "return_keys"
    loaned_out_date = Column('loaned_out_date', DateTime,nullable=False, primary_key=True)
    request_request_id = Column('request_id', Integer, ForeignKey('requests.request_id'), nullable=False, primary_key=True)
    return_date = Column('return_date', DateTime(timezone=False), default=func.now(), nullable=False, primary_key=True)

    requests = relationship("Requests", back_populates="returnkeys")

    # Constructor
    def __init__(self, request, loaned_date: DateTime):
        self.loaned_out_date = loaned_date
        self.request_request_id = request.request_request_id
