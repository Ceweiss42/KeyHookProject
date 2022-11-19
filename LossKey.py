# new
import datetime

from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime, ForeignKeyConstraint  # new
from sqlalchemy.orm import relationship

from KeyIssuance import KeyIssuances

from orm_base import Base


class LossKeys(Base):
    __tablename__ = "loss_keys"
    key_issuance_loaned_out_date = Column('loaned_out_date', DateTime, #ForeignKey('key_issuance.loaned_out_date'),
                                           nullable=False, primary_key=True)
    key_issuance_request_id = Column('request_id', Integer, #ForeignKey('key_issuance.request_id'),
                                      nullable=False, primary_key=True)
    loss_date = Column('loss_date', DateTime, nullable=False, primary_key=True)

    ForeignKeyConstraint(['loaned_out_date', 'request_id'], ['key_issuances.loaned_out_date', 'key_issuances.request_id'], name="fk_losskeys_keyissuance_01")

    key_issuance = relationship("key_issuance", back_populates = "loss_key")

    # Constructor
    def init(self, key_issuance: KeyIssuances, loss_date: DateTime):
        self.key_issuance_loaned_out_date = key_issuance.loaned_out_date
        self.key_issuance_request_id= key_issuance.request_request_id
        self.loss_date = loss_date
