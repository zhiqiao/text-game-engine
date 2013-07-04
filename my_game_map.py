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
          AssertionError if the dimensions have not been set.
        """
        assert self.height and self.width
        self._game_map = []
        for h in range(self.height):
            self.game_map.append([None] * self.width)

    def SetRoom(self, y, x, contents):
        """Define the contents of a room.

        Contents to place at the coordinate must at least implement the
        following:
          __str__

        Args:
          y:  Y-coordinate of the room to set.
          x:  X-coordinate of the room to set.
          contents:  Object to place at (y, x).  Should be of type
            my_game_room.GameRoom.

        Returns:
          Object set at coordinate on map.

        Raises:
          AssertionError if you try to set a value which is outside the
            dimensions of the map.
        """
        assert y >= 0 and y < self.height
        assert x >= 0 and x < self.width
        self.game_map[y][x] = contents
        return self.game_map[y][x]

    def GetRoom(self, y, x):
        """Get object at location.

        Args:
          y:  Y-coordinate of the room to set.
          x:  X-coordinate of the room to set.

        Returns:
          Object set at coordinate on map including None if the object at that
          coordinate has not been defined.

        Raises:
          AssertionError if you try to get a value which is outside the
            dimensions of the map.
        """
        assert y >= 0 and y < self.height
        assert x >= 0 and x < self.width
        return self.game_map[y][x]
    
    def DebugInfo(self):
        """Debug method to visualize current state of game board."""
        output_rows = []
        for h in range(self.height):
            curr_row = []
            for w in range(self.width):
                if self.game_map[h][w] is not None:
                    curr_row.append(str(self.game_map[h][w]))
                else:
                    curr_row.append("#")
            output_rows.append("".join(curr_row))
        return output_rows

    def PrintDebugOutput(self, height, width, debug_output):
        print "-" * (width + 2)
        for r in debug_output:
            print "|%s|" % r
        print "-" * (self.width + 2)
