from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from KeyIssuance import KeyIssuances

from orm_base import Base


class ReturnKeys(Base):
    __tablename__ = "return_keys"
    key_issuance_loaned_out_date = Column('loaned_out_date', DateTime, ForeignKey('key_issuances.loaned_out_date'), nullable=False, primary_key=True)
    key_issuance_request_id = Column('request_id', Integer, ForeignKey('key_issuances.request_id'), nullable=False, primary_key=True)
    return_date = Column('return_date', DateTime, nullable=False, primary_key=True)

    key_issuance = relationship("key_issuance", back_populates = "return_keys")

    # Constructor
    def init(self, key_issuance: KeyIssuances, return_date: DateTime):
        self.key_issuance_loaned_out_date = key_issuance.loaned_out_date
        self.key_issuance_request_id = key_issuance.request_request_id
        self.return_date = return_date
