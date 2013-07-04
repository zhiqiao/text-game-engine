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
        # Inventory is sorted.
        self._inventory = []
        self._max_inventory_size = 0
        self._room_state_mapper = None
        self._item_mapper = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        self._name = n

    @property
    def game_map(self):
        return self._game_map

    @game_map.setter
    def game_map(self, m):
        self._game_map = m

    @property
    def curr_room(self):
        return self._curr_room

    @curr_room.setter
    def curr_room(self, r):
        self._curr_room = r

    @property
    def y_pos(self):
        return self._y_pos

    @y_pos.setter
    def y_pos(self, y):
        self._y_pos = y

    @property
    def x_pos(self):
        return self._x_pos

    @x_pos.setter
    def x_pos(self, x):
        self._x_pos = x

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, i):
        self._inventory = i

    @property
    def max_inventory_size(self):
        return self._max_inventory_size

    @max_inventory_size.setter
    def max_inventory_size(self, s):
        self._max_inventory_size = s

    @property
    def room_state_mapper(self):
        return self._room_state_mapper

    @room_state_mapper.setter
    def room_state_mapper(self, m):
        self._room_state_mapper = m

    @property
    def item_mapper(self):
        return self._item_mapper

    @item_mapper.setter
    def item_mapper(self, m):
        self._item_mapper = m

    def Start(self):
        """Check the player is on a valid game map and a valid room.

        Must be called before starting the game.

        Returns:
          True iff the player has:
          - a valid game map AND
          - an Y-coordinate AND
          - an X-coordinate AND
          - (Y, X) is a valid room in the map AND
          - a valid item mapper is attached AND
          - a valid state mapper is attached
          False otherwise
        """
        if self._game_map:
            self._curr_room = self._game_map.GetRoom(self._y_pos, self._x_pos)
            if (self._curr_room is not None
                and self._room_state_mapper
                and self._item_mapper):
                return True
        return False
        
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

        Inventory is stored in sorted order.

        Args:
          item:  String name of item add to inventory.

        Returns:
          True iff player inventory has space and item was successfully added
          to inventory.
        """
        if len(self._inventory) < self._max_inventory_size:
            self._inventory.append(item)
            self._inventory.sort()
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
        dropped_item = my_game_utils.RemoveContent(self._inventory, item)
        if dropped_item is None:
            return False
        # This assumes the curr_room exists, which may not always be the case.
        # However, as this is part of gameplay, it is unlikely to get there from
        # outside the command interface.
        self._curr_room.AddContent(dropped_item)
        return True

    def UseItem(self, item):
        """Attempt to use an item from player inventory.

        If the item exists in the player's inventory and is not reusable, it is
        removed from the inventory regardless of it's effect on the room.

        Args:
          item:  String name of item to remove and used from inventory.

        Returns:
          True iff player inventory has given item and it was used successfully,
          i.e. it had some effect on the room.  False otherwise.
        """
        # Temporarily remove the item.
        item = my_game_utils.RemoveContent(self._inventory, item)
        if item is None:
            return False
        item_obj = self._item_mapper.GetItem(item)
        # Put item back if it is reusable.
        if item_obj.reusable:
            self.AddItem(item)
        new_state = item_obj.UseItem(self._curr_room.state)
        return self._curr_room.TryChangeState(new_state)

    def GetRoomDisplay(self):
        """Return readable details of the current room."""
        # You can't inspect the room if you are in an invalid state, but by then
        # Start() could not have been called.
        return self._room_state_mapper.GetState(self._curr_room.state)

    def GetRoomContentsDisplay(self):
        """Return readable contents of the current room."""
        return my_game_utils.GetContentsDisplay(self._curr_room.contents)

    def GetInventoryDisplay(self):
        """Return readable details of current inventory."""
        return my_game_utils.GetContentsDisplay(self._inventory)

    def Inspect(self):
        """Return readable details of current inventory and room as a dict."""
        return {"room": self.GetRoomDisplay(),
                "room_contents": self.GetRoomContentsDisplay(),
                "inventory": self.GetInventoryDisplay()
               }
