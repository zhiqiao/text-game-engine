import functools
import re

import my_game_interface
import my_game_item
import my_game_map
import my_game_player
import my_game_room


class ParseError(Exception):
    pass


class GameParser(object):
    """Parser for the game configuration.

    After this class finishes parsing the config file, a my_game_player.Player
    and a my_game_interface.GameInterface will be ready to start the game.
    """

    SECTION_RE = re.compile(r"^\[([A-Z_]+)\]$")

    def __init__(self):
        self._curr_section = None
        self._section_lines = []  # A list of lines in the current [SECTION]
        self._game_interface = my_game_interface.GameInterface()
        self._player = my_game_player.Player()

    @property
    def curr_section(self):
        return self._curr_section

    @curr_section.setter
    def curr_section(self, s):
        # Create a setter for testing.
        self._curr_section = s

    @property
    def section_lines(self):
        return self._section_lines

    @section_lines.setter
    def section_lines(self, lines):
        # Create a setter for testing.
        self._section_lines = lines

    @property
    def game(self):
        return self._game

    @property
    def game_interface(self):
        return self._game_interface

    @property
    def player(self):
        return self._player

    def Parse(self, filename):
        with open(filename, "r") as f:
            for line in f:
                self.ParseLine(line)
            # Parse last section.
            self.ParseSection(self._curr_section)

    def ParseGameLine(self, line_parts):
        """Parse a line from the [GAME] section of the config.

        Args:
          line_parts:  An array of the config file line, split on ":".

        Raises:
          ParseError if the key of the config line is not one of:
            name
            exposition
            help
            player_inventory
            player_inventory_capacity
        """
        key = line_parts[0].strip().lower()
        if key == "name":
            self._game_interface.name = line_parts[1]
        elif key == "exposition":
            self._game_interface.exposition = line_parts[1].strip()
        elif key == "help":
            self._game_interface.help = line_parts[1].strip()
        elif key == "player_inventory":
            for item in line_parts[1:]:
                # We can't use Player.AddItem here because the player's current
                # room hasn't been fully initialized.  We are not adding items
                # from the room, but from the initial game state.
                self._player.inventory.append(item)
        elif key == "player_inventory_capacity":
            self._player._max_inventory_size = int(line_parts[1])
        else:
            raise ParseError(
                "Unrecognized line in [GAME] section: %s", line_parts)

    def ParseRoomState(self, line_parts):
        """Parse [ROOM_STATES] section of config file.

        Assumes lines of the form "<ID>:<colon-separated list of descriptions>

        Args:
          line_parts:  An array of the config file line, split on ":".

        Raises:
          ParseError if we are unable to convert the expected item ID into an
          int.
        """
        try:
            key = int(line_parts[0])
        except ValueError:
            raise ParseError(
                "Unrecognized line in [ROOM_STATES] section: %s", line_parts)
        self.player._room_state_mapper.AddState(
            key, [p.strip() for p in line_parts[1:]])

    def ParseItem(self, line_parts):
        """Parse [ITEMS] section of config file.

        Assumes lines of the form:
          <name>:<colon-separated list of state-changing effects>
        where state-changing effect is of the form "old_state_id>new_state_id".

        Args:
          line_parts:  An array of the config file line, split on ":".

        Raises:
          ParseError if we are unable to parse a state-changing effect specified.
        """
        key = line_parts[0]
        item = my_game_item.GameItem()
        for effect in line_parts[1:]:
            try:
                old_state, new_state = [int(s) for s in effect.split(">")]
            except ValueError:
                raise ParseError(
                    "Error parsing effect for %s: %s", key, effect)
            item.AddStateChange(old_state, new_state)
        self._player.item_mapper.AddItem(key, item)

    def ParseMapPoint(self, line_parts):
        """Helper function to ParseMap to parse map points.

        Map points are of the form:
          <Y pos>:<X pos>:state ID:<colon-separated list of item names>
        Args:
          line_parts:  An array of the config file line, split on ":".

        Raises:
          ParseError if we are unable to parse the map point.
        """
        try:
            y = int(line_parts[0])
            x = int(line_parts[1])
            state = int(line_parts[2])
            items = line_parts[3:]
        except ValueError:
            raise ParseError("Unable to parse map point: %s", line_parts)
        
        new_room = my_game_room.Room()
        new_room.state = state
        for i in items:
            if i:
                new_room.AddContent(i)
        self._player.game_map.SetRoom(y, x, new_room)

    def ParseMap(self, line_parts):
        """Parse the [MAP] section of the config.

        This section contains the following fields in order.  They must be in
        order or the map will fail to parse.
          height
          width
          player_start
          as well as a series of lines to define the rooms on the map

        Args:
          line_parts:  An array of the config file line, split on ":".

        Raises:
          ParseError if we are unable to parse the line.
        """
        key = line_parts[0]
        try:
            if key == "dimensions":
                self._player.game_map.height = int(line_parts[1])
                self._player.game_map.width = int(line_parts[2])
                self._player.game_map.Initialize()
            elif key == "player_start":
                self._player.y_pos = int(line_parts[1])
                self._player.x_pos = int(line_parts[2])
            else:
                self.ParseMapPoint(line_parts)
        except ValueError:
            raise ParseError(
                "Unrecognized line in [MAP] section: %s", line_parts)
        except my_game_map.GameMapError, e:
            raise ParseError("Unable to initialize map after parsing:\n%s", e)

    def ParseAlias(self, alias, line_parts):
        """Parse the [ALIASES_*] sections of the config.

        These are aliases for both action verbs and directions.  These are then
        mapped to possible player actions.

        Args:
          line_parts:  An array of the config file line, split on ":".
        """
        key = line_parts[0]
        if alias == "MOVE":
            self._game_interface.AddMoveAlias(key)
        elif alias == "UP":
            self._game_interface.AddDirectionAlias(
                key, my_game_player.Player.MoveUp)
        elif alias == "DOWN":
            self._game_interface.AddDirectionAlias(
                key, my_game_player.Player.MoveDown)
        elif alias == "LEFT":
            self._game_interface.AddDirectionAlias(
                key, my_game_player.Player.MoveLeft)
        elif alias == "RIGHT":
            self._game_interface.AddDirectionAlias(
                key, my_game_player.Player.MoveRight)
        elif alias == "USE":
            self._game_interface.AddActionAlias(
                key, my_game_player.Player.UseItem)
        elif alias == "ADD":
            self._game_interface.AddActionAlias(
                key, my_game_player.Player.AddItem)
        elif alias == "DROP":
            self._game_interface.AddActionAlias(
                key, my_game_player.Player.DropItem)
        elif alias == "INSPECT":
            self._game_interface.AddActionAlias(
                key, my_game_player.Player.Inspect)
        else:
            raise ParseError("Unrecognized ALIASES section: %s", alias)

    def ParseSection(self, section):
        """Parses current set of config lines under the named section.

        Args:
          section:  String name for section to parse.

        Raises:
          ParseError: if we are unable to initialize the game map, probably due
          to the [MAP] section occuring before the [GAME] section.
        """
        if not section:
            # This is the first section we have encountered.
            return
        for line in self._section_lines:
            line_parts = line.strip().split(":")
            if section == "GAME":
                self.ParseGameLine(line_parts)
            elif section == "ROOM_STATES":
                self.ParseRoomState(line_parts)
            elif section == "ITEMS":
                self.ParseItem(line_parts)
            elif section == "MAP":
                self.ParseMap(line_parts)
            elif section.startswith("ALIASES_"):
                alias = section.replace("ALIASES_", "")
                self.ParseAlias(alias, line_parts)
    
    def ParseLine(self, line):
        if not line.strip() or line.startswith("#"):
            # Ignore empty lines and comments.
            return
        match = self.SECTION_RE.match(line)
        if match:
            self.ParseSection(self._curr_section)
            self._curr_section = match.group(1) 
            self._section_lines = []
        else:
            self._section_lines.append(line)
