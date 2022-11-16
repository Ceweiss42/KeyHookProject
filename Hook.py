from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint
from sqlalchemy.orm import relationship
from HookDoor import HookDoor
from orm_base import Base


class Hook(Base):
    __tablename__ = "hooks"
    hook_number = Column('hook_number', Integer, Identity(start=1, cycle=True),
                         nullable=False, primary_key=True)

    # Hook does not have a candidate key
    # Many to many relationship with HookDoor
    door_list: [HookDoor] = relationship("HookDoor", back_populates="hook", viewonly=False)

    def __init__(self, hook):
        self.hook_number = hook.hook_number
        self.door_list = []

    """Add an door to the list of hooks.
        @param door The instance of door tied to this hook."""

    def add_door(self, door):
        # make sure this request is non already on the list.
        for next_door in self.door_list:
            if next_door == door:
                # message stating that the request has already made
                print("Door already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        hook_door = HookDoor(self, door)
        # Update this move to reflect that we have this request.
        door.hook_list.append(hook_door)
        # Update the genre to reflect this request.
        self.door_list.append(hook_door)