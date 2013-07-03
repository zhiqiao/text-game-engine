
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
        self._game_map = []
        self._height = 0
        self._width = 0

    @property
    def game_map(self):
        return self._game_map

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, h):
        self._height = h

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, w):
        self._width = w

    def Initialize(self):
        """Initialize the game map to just the empty dimensions."""
        for h in range(self.height):
            self.game_map.append([None] * self.width)

    def SetRoom(self, y, x, contents):
        """Define the contents of a room.

        Contects to place at the coordinate must at least implement the
        following:
          __str__

        Args:
          y:  Y-coordinate of the room to set.
          x:  X-coordinate of the room to set.
          contents:  Object to place at (y, x).
        """
        self.game_map[h][w] = contents
    
    def PrintDebug(self):
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
        print "-" * (self.width + 2)
        for r in output_rows:
            print "|%s|" % r
        print "-" * (self.width + 2)


def main():
    gm = GameMap()
    gm.width = 10
    gm.height = 8
    gm.Initialize()
    gm.SetRoom(0, 0, "A")
    gm.SetRoom(1, 0, "B")
    gm.SetRoom(0, 1, "C")
    gm.SetRoom(1, 1, " ")
    gm.SetRoom(4, 4, " ")
    gm.SetRoom(5, 4, " ")
    gm.SetRoom(4, 5, " ")
    gm.PrintDebug()


if __name__ == "__main__":
    main()
