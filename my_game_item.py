import copy

class ItemMapper(object):
    """Class to maintain all possible game items.

    This class, when instantiated, acts like a datastore mapping between a game
    item name and a copy of that game item.
    """

    def __init__(self):
        # A default no-op item.
        self._default_item = GameItem()
        self._all_items = {}

    @property
    def all_items(self):
        return self._all_items

    @property
    def default_item(self):
        return self._default_item

    @default_item.setter
    def default_item(self, i):
        self._default_item = i

    def AddItem(self, name, item):
        """Add or potentially override an existing entry with a copy of item.

        Args:
          name:  String name of item.
          item:  A GameItem object.
        """
        self._all_items[name] = copy.deepcopy(item)

    def GetItem(self, name):
        """Returns the named item.

        Caller takes control of the returned object.

        Args:
          name:  Name of item to get.
        
        Returns:
          A copy of the stored item if found.  Otherwise, returns the default
          item.
        """
        return copy.deepcopy(self._all_items.get(name, self._default_item))


class GameItem(object):
    """A game item.

    A game item is modelled as something which allows the player to change
    the state of a room s/he is in.  The possible room state changes are stored
    in a dict.  If the state of the room where the item is being used does not
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

    def UseItem(self, curr_state):
        """Attempt to use this item affect the given state.

        Check to see if the curr_state is included in this item's possible
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

    def DebugInfo(self):
        output = []
        for old_state, new_state in self._state_changes.iteritems():
            output.append("change %d to %d" % (old_state, new_state))
        return ["%s can:" % self._name] + sorted(output) + [
            "reusable: %s" % ("yes" if self._reusable else "no")]
                  
        
