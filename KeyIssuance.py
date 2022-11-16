from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship


from orm_base import Base


class KeyIssuances(Base):
    __tablename__ = "key_issuances"
    loaned_out_date = Column('loaned_out_date', DateTime , nullable=False, primary_key=True)
    request_request_id = Column('request_id', Integer, ForeignKey('requests.request_id'), nullable=False, primary_key=True)

    loss_keys = relationship("loss_keys", back_populates="key_issuance", uselist=False)
    return_keys = relationship("return_keys", back_populates="key_issuance", uselist=False)

    # Constructor
    def init(self, loaned_out_date: DateTime, request):
        self.loaned_out_date = loaned_out_date
        self.request_request_id = request.request_id
