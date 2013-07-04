class ObjectMapper(object):
    """Class to maintain all possible game objects.

    This class, when instantiated, acts like a datastore mapping between a game
    object name and a copy of that game object.
    """
    pass


class GameObject(object):
    """A game object.

    A game object is modelled as something which allows the player to change
    the state of a room s/he is in.  The possible room state changes are stored
    in a dict.  If the state of the room where the object is being used does not
    have an entry in this dict, there is no effect and the state remains
    unchanged.
    """

    def __init__(self):
        self._name = None
        self._state_changes = {}
        self.reusable = True

    def __eq__(self, o):
        return self._name == o.name

    @property
    def sort_id(self):
        return self._name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def reusable(self):
        return self._reusable

    @reusable.setter
    def reusable(self, n):
        self._reusable = n

    def AddStateChange(self, old_state, new_state):
        """Add or update ability to change a room from old_state to new_state.

        Args:
          old_state:  Integer ID for room state.
          new_state:  Integer ID for room state.
        """
        self._state_changes[old_state] = new_state

    def __str__(self):
        return self._name

    def UseObject(self, curr_state):
        """Attempt to use this object affect the given state.

        Check to see if the curr_state is included in this object's possible
        state_changes.

        Args:
          curr_state:  Integer ID of the current state.

        Returns:
          The new state ID if curr_state is in state_changes, the same
          curr_state if not.
        """
        if curr_state in self._state_changes:
            return self._state_changes[curr_state]
        return curr_state