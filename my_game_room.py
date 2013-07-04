class RoomState(object):
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
        return str(self.sid)


class RoomStateMapper(object):
    """Class to maintain all configured room states.

    This class, when instantiated, acts like a datastore mapping between a state
    ID and a description of a room.
    """

    def __init__(self):
        self._all_states = {}

    @property
    def all_states(self):
        return self._all_states

    def AddState(self, sid, desc):
        """Add or potentially override an existing room state description.

        Args:
          sid:  Integer room state ID.
          desc:  String description.
        """
        self._all_states[sid] = desc

    def GetState(self, sid):
        """Returns the description of the game state.

        Args:
          sid:  Integer room state ID.
        
        Returns:
          A string description of the room state, None if the ID does not exist
          in the mapping.
        """
        return self._all_states.get(sid, None)


class GameRoom(object):
    """Object to abstract out concept of a room in the game."""
    
    def __init__(self):
        # A state class must implement a __str__ method for debugging.
        self._state = None
        # Contents are kept sorted.
        # Every content class must implement a __str__ method for debugging.
        # Every content class must implement an sort_id method to be able to
        # order these objects.
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
        """Add content to this room.

        Takes ownership of the object.

        Args:
          c:  Name of an object to put into the room.

        Raises:
          Attribute error if sort_id is undefined.
        """
        self._contents.append(c)
        self._contents.sort()

    def RemoveContent(self, content_name):
        """Remove content object from the room.

        Args:
          content_name: Name of the object to be removed from the room.

        Returns:
          The object if found, None otherwise.
        """
        for i, c in enumerate(self._contents):
            if c == content_name:
                break
        if i == len(self._contents)-1 and c != content_name:
            return None
        # Removing an object from a sorted list should still preserve the sorted
        # order of the list.
        return self._contents.pop(i)

    def GetContentsDisplay(self):
        """Get the contents of the room to display.

        Returns:
           A list of strings of the form "NxNAME" where N is the number of that
           object in the room.  [] if there are no objects in the room.
        """
        output = []
        curr = None
        count = 0
        # The reason for this algorithm for counting objects, with assuming they
        # are sorted, as opposed to using a dict, is because the results should
        # be sorted by name of object, which would be difficult to do after
        # flattening a dict.
        for c in self.contents:
            if curr is None:
                curr = c
            if c != curr:
                output.append("%dx%s" % (count, curr))
                curr = c
                count = 1
            else:
                count += 1
        if count:
            output.append("%dx%s" % (count, c))
        return output

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
