import my_game_utils


class RoomStateMapper(object):
    """Class to maintain all configured room states.

    This class, when instantiated, acts like a datastore mapping between a state
    ID and a description of a room, which is a list of adjectives.
    """

    def __init__(self):
        self._default_state = []
        self._all_states = {}

    @property
    def all_states(self):
        return self._all_states

    @property
    def default_state(self):
        return self._default_state

    @default_state.setter
    def default_state(self, s):
        self._default_state = s

    def AddState(self, sid, desc):
        """Add or potentially override an existing room state description.

        Args:
          sid:  Integer room state ID.
          desc:  List of string descriptions.
        """
        self._all_states[sid] = desc

    def GetState(self, sid):
        """Returns the description of the game state.

        Args:
          sid:  Integer room state ID.
        
        Returns:
          A list of string descriptions of the room state, the default state if
          the ID does not exist in the mapping.
        """
        return self._all_states.get(sid, self._default_state)


class Room(object):
    """Object to abstract out concept of a room in the game."""
    
    def __init__(self):
        # A state class must implement a __str__ method for debugging.
        self._state = None
        # Contents are kept sorted.
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

    @contents.setter
    def contents(self, c):
        self._contents = c

    def AddContent(self, item):
        """Add content to this room.

        Takes ownership of the item.

        Args:
          item:  Name of an item to put into the room.

        Raises:
          Attribute error if sort_id is undefined.
        """
        self._contents.append(item)
        self._contents.sort()

    def RemoveContent(self, content_name):
        # Removing an item from a sorted list should still preserve the sorted
        # order of the list.
        return my_game_utils.RemoveContent(self._contents, content_name)

    def GetContentsDisplay(self):
        """Get the contents of the room to display."""
        return my_game_utils.GetContentsDisplay(self._contents)

    def TryChangeState(self, new_state):
        if new_state == self._state:
            return False
        self._state = new_state
        return True

    def __str__(self):
        return self.state.sid

    def DebugInfo(self):
        """Returns a list of debug info."""
        return ["STATE: %s" % str(self.state),
                "CONTENTS: [%s]" % ", ".join(self.GetContentsDisplay())
               ]
