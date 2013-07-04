# Specific imports
import my_game_utils

class Player(object):
    """Representation of a player in the game.

    All in-game actions should be represented by this object.
    """

    def __init__(self):
        self._name = None
        self._game_map = None
        self._curr_room = None
        self._y_pos = None
        self._x_pos = None
        self._inventory = []
        self._max_inventory_size = 0
        self._room_state_mapper = None

    @proprety
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @proprety
    def game_map(self):
        return self._game_map

    @game_map.setter
    def game_map(self, m):
        self._game_map = m

    @proprety
    def curr_room(self):
        return self._curr_room

    @curr_room.setter
    def curr_room(self, r):
        self._curr_room = r

    @proprety
    def y_pos(self):
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y):
        self._y_pos = y

    @proprety
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x):
        self._x_pos = x

    @proprety
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, i):
        self._inventory = i

    @proprety
    def max_inventory_size(self):
        return self._max_inventory_size

    @max_inventory_size.setter
    def max_inventory_size(self, s):
        self._max_inventory_size = s

    @proprety
    def room_state_mapper(self):
        return self._room_state_mapper

    @room_state_mapper.setter
    def room_state_mapper(self, m):
        self._room_state_mapper = m

    def Move(self, new_y, new_x):
        """Move in the specified direction if you are able to.

        Args:
          new_y:  Integer Y-coordinate.
          new_x:  Integer X-coordinate.

        Returns:
          True iff you are able to move to the target coordinate.  False
          otherwise.
        """
        new_room = self.game_map.GetRoom(new_y, new_x)
        if new_room is None:
            return False
        self._y_pos = new_y
        self._x_pos = new_x
        self._curr_room = new_room
        return True

    def MoveUp(self):
        return self.Move(self._y_pos-1, self._x_pos)

    def MoveDown(self):
        return self.Move(self._y_pos+1, self._x_pos)
    
    def MoveLeft(self):
        return self.Move(self._y_pos, self._x_pos-1)

    def MoveRight(self):
        return self.Move(self._y_pos, self._x_pos+1)

    def AddItem(self, item):
        """Attempt to add an item to player inventory.

        Args:
          item:  String name of item add to inventory.

        Returns:
          True iff player inventory has space and item was successfully added
          to inventory.
        """
        if len(self._inventory) < self._max_inventory_size:
            self._inventory.append(item)
            return True
        return False

    def DropItem(self, item):
        """Attempt to drop an item from player inventory and add it to the room.

        Args:
          item:  String name of item remove from inventory.

        Returns:
          True iff player inventory has given item and it was successfully
          removed from inventory and added to the room's contents.
        """
        dropped_item = my_game_utils.RemoveContent(item)
        if dropped_item is None:
            return False
        self._curr_room.AddContent(dropped_item)
        return True

    def UseItem(self, item):
        """Attempt to use an item from player inventory.

        If the item exists in the player's inventory and is not reusable, it is
        removed from the inventory regardless of it's effect on the room.

        Args:
          item:  String name of item remove from inventory.

        Returns:
          True iff player inventory has given item and it was used successfully,
          i.e. it had some effect on the room.  False otherwise.
        """
        
        return bool(my_game_utils.RemoveContent(item))

    def InspectRoom(self):
        return self._room_state_mapper.GetRoomDisplay(self._curr_room.state)

    def GetInventoryDisplay(self):
        return my_game_utils.GetContentsDisplay(self._inventory)

    def Inspect(self):
        pass
