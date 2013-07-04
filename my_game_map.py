class GameMapError(Exception):
    pass

class GameMap(object):
    """Object representing game map state.

    The map is represented by a two-dimensional list with the origin at the top
    left hand corner.  Each room has an (y, x) coordinate to facilitate easier
    spacial reasoning, i.e.:

    (0, 0) -----------------> (0, w)
      |                         |
      |                         |
      |                         |
      |                         |
      V                         V
    (h, 0) -----------------> (h, w)
    """

    def __init__(self):
        self._game_map = None
        self._height = None
        self._width = None

    @property
    def game_map(self):
        return self._game_map

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):
        assert h > 0
        self._height = h

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, w):
        assert w > 0
        self._width = w

    def Initialize(self):
        """Initialize an empty game map with the current dimensions.

        Raises:
          GameMapError if the dimensions have not been set.
        """
        if not self.height or not self.width:
            raise GameMapError("Map is not set")
        self._game_map = []
        for h in range(self.height):
            self.game_map.append([None] * self.width)

    def SetRoom(self, y, x, room):
        """Define the room at a given coordinate.

        Room to place at the coordinate must at least implement the
        following:
          __str__

        Args:
          y:  Y-coordinate of the room to set.
          x:  X-coordinate of the room to set.
          room:  Object to place at (y, x).  Should be of type
            my_game_room.GameRoom.

        Returns:
          Object set at coordinate on map.

        Raises:
          GameMapError if you try to set a value which is outside the
            dimensions of the map.
        """
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            raise GameMapError("Invalid space (%d, %d)", y, x)
        self.game_map[y][x] = room
        return self.game_map[y][x]

    def GetRoom(self, y, x):
        """Get object at location.

        Args:
          y:  Y-coordinate of the room to set.
          x:  X-coordinate of the room to set.

        Returns:
          Object set at coordinate on map including None if the object at that
          coordinate has not been defined or if the request position is out of
          bounds.
        """
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            return None
        return self.game_map[y][x]
    
    def DebugInfo(self, y_player=None, x_player=None):
        """Debug method to visualize game board."""
        output_rows = []
        for y in range(self.height):
            curr_row = []
            for x in range(self.width):
                if self.game_map[y][x] is not None:
                    if (y_player is not None
                        and x_player is not None
                        and y == y_player
                        and x == x_player):
                        curr_row.append("P")
                    else:
                        curr_row.append(" ")
                else:
                    curr_row.append("#")
            output_rows.append("".join(curr_row))
        return output_rows

    def PrintDebugOutput(self, y_player=None, x_player=None):
        print "+%s+" % ("-" * self.width)
        for r in self.DebugInfo(y_player=y_player, x_player=x_player):
            print "|%s|" % r
        print "+%s+" % ("-" * self.width)
