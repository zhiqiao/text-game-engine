class RoomState(self):
    """Object to abstract out concept of a room's state."""

    def __init__(self):
        self._sid = None
        self._desc = None

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, i):
        self._sid = i

    @property
    def desc(self):
        return self._desc

    @desc.setter
    def desc(self, d):
        self._desc = d

    def __str__(self):
        return "ID: %s (%d)" % (self.desc, self.sid)

    def PrintDebug(self):
        


class RoomStateMapper(object):
    """Class to maintain all configured room states.

    This class, when instantiated, acts like a datastore mapping between a state
    ID and a description of a room.
    """

    def __init__(self):
        self._sid_to_state = {}

    def AddState(self, sid, desc):
        """Add or potentially override an existing room state description.

        Args:
          sid:  Integer room state ID.
          desc:  String description.
        """
        self._sid_to_state[sid] = desc

    def GetState(self, sid):
        """Returns the description of the game state.

        Args:
          sid:  Integer room state ID.
        
        Returns:
          A string description of the room state, None if the ID does not exist
          in the mapping.
        """
        return self._sid_to_state.get(sid, None)


class GameRoom(object):
    """Object to abstract out concept of a room in the game."""
    
    def __init__(self):
        # A state class must implement a __str__ method for debugging.
        self._state = None
        # Every content class must implement a __str__ method for debugging.
        self._contents = []
    
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, s):
        self._state = s

    @property
    def contents(self):
        return self._contents

    def AddContent(self, c):
        self.contents.append(c)

    def ChangeState(self, game_object):
        """Attempt to apply a game object to the state of the room.

        Check if the game object can affect the state of the room.  If it can,
        change the state of this room.  Otherwise, do nothing.

        Args:
          game_object:  A my_game_object.GameObject object.

        Returns:
          True if the game_object can affect the state of the room, False
          otherwise.
        """
        curr_state = self.state
        self.state = game_object.UseObject(self.state)
        return curr_state != self.state

    def __str__(self):
        return self.state.sid

    def DebugInfo(self):
        """Returns a list of debug info."""
        return ["STATE: %s" % str(self.state),
                "CONTENTS: [%s]" % ", ".join(
                [str(c) for c in self.contents])
               ]
