# new
import datetime

from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime  # new
from sqlalchemy.orm import relationship

from KeyIssuance import KeyIssuance

from orm_base import Base


class LossKey(Base):
    __tablename__ = "loss_keys"
    key_issuance_loaned_out_date = Column('loaned_out_date', DateTime, ForeignKey('key_issuances.loaned_out_date'), nullable=False, primary_key=True)
    key_issuance_request_id = Column('request_id', Integer, ForeignKey('key_issuances.request_id'), nullable=False, primary_key=True)
    loss_date = Column('loss_date', DateTime, nullable=False, primary_key=True)

    key_issuance = relationship("key_issuance", back_populates = "loss_keys")

    # Constructor
    def init(self, key_issuances, loss_date: DateTime):
        self.key_issuance_loaned_out_date = key_issuances.loaned_out_date
        self.key_issuance_request_id= key_issuances.request_request_id
        self.loss_date = loss_date
