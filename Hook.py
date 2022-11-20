from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, Sequence
from sqlalchemy.orm import relationship
from orm_base import Base


# from Key import Keys
from HookDoor import HookDoors


class Hooks(Base):
    __tablename__ = "hooks"
    hook_number = Column('hook_number', Integer, Identity("hook_seq", start=1),
                         nullable=False, primary_key=True)

    doors_list: [HookDoors] = relationship("HookDoors", back_populates="hooks")

    keys = relationship("Keys", back_populates="hooks")
    # Hook does not have a candidate key
    # Hook is not a child to a relationship.
    #   door_list: [HookDoors] = relationship("HookDoor", back_populates="hook", viewonly=False)
    #   key = relationship("Key", back_populates="hook", viewonly=False)


    def __init__(self):
        pass


#        self.door_list = []


#    """#Add an door to the list of hooks.
#        @param door The instance of door tied to this hook."""
    def add_door(self, door):
        # make sure this request is non already on the list.
        for next_door in self.doors_list:
            if next_door == door:
                # message stating that the request has already made
                print("Door already exist.")
                return
        # Create an instance of the junction table class for this relationship.
        hook_door = HookDoors(self, door)
        # Update this move to reflect that we have this request.
        door.hooks_list.append(hook_door)
        # Update the genre to reflect this request.
        self.doors_list.append(hook_door)


