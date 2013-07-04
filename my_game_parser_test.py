import unittest

import my_game_parser


class TestGameParser(unittest.TestCase):
    
    def setUp(self):
        self._game_parser = my_game_parser.GameParser()

    def test_parse_game_section(self):
        self._game_parser.section_lines = [
            "name:ISS Fire",
            "exposition: Test game.",
            "player_inventory_capacity:10",
            "player_inventory:foam:foam:foam:CO2:CO2",
            "noun_room:section",
            "noun_up:bow",
            "noun_down:stern",
            "noun_left:port",
            "noun_right:starboard",
            ]
        self._game_parser.ParseSection("GAME")
        player = self._game_parser.player
        game_interface = self._game_parser.game_interface
        self.assertEqual(
            game_interface.DebugInfo(),
            ["GAME: ISS Fire",
             "EXPOSITION: Test game.",
             ("NOUNS: room=section,"
              " up=bow, down=stern, left=port, right=starboard")])
        self.assertEqual(player.max_inventory_size, 10)
        self.assertEqual(player.GetInventoryDisplay(), ["2xCO2", "3xfoam"])

    def test_parse_room_states(self):
        self._game_parser.section_lines = [
            "0:fine",
            "1: electrical fire",
            "2:fabric fire ",
            "3:electrical fire : fabric fire",
            ]
        self._game_parser.ParseSection("ROOM_STATES")
        room_state_mapper = self._game_parser.player.room_state_mapper
        self.assertEqual(room_state_mapper.GetState(0), ["fine"])
        self.assertEqual(room_state_mapper.GetState(1), ["electrical fire"])
        self.assertEqual(room_state_mapper.GetState(2), ["fabric fire"])
        self.assertEqual(room_state_mapper.GetState(3),
                         ["electrical fire", "fabric fire"])
        self.assertEqual(room_state_mapper.GetState(4), [])
        # Can't parse a non-int type for key.
        self._game_parser.section_lines = ["'0':fine"]
        with self.assertRaises(my_game_parser.ParseError):
            self._game_parser.ParseSection("ROOM_STATES")
        # OK to parse extraneous colons.
        self._game_parser.section_lines = ["0:fine:"]
        self._game_parser.ParseSection("ROOM_STATES")

    def test_parse_items(self):
        self._game_parser.section_lines = [
            "water:1>0",
            "foam:2>1:1>0",
            "CO2:3>1:2>0",
            ]
        self._game_parser.ParseSection("ITEMS")
        item_mapper = self._game_parser.player.item_mapper
        water = item_mapper.GetItem("water")
        self.assertEqual(item_mapper.GetItem("water").UseItem(1), 0)
        self.assertEqual(item_mapper.GetItem("foam").UseItem(2), 1)
        self.assertEqual(item_mapper.GetItem("CO2").UseItem(3), 1)
        self.assertEqual(item_mapper.GetItem("co2").UseItem(3), 3)
        self._game_parser.section_lines = ["water:1>0>2"]
        with self.assertRaises(my_game_parser.ParseError):
            self._game_parser.ParseSection("ITEMS")
        # Can't parse items without effects.
        self._game_parser.section_lines = ["water:"]
        with self.assertRaises(my_game_parser.ParseError):
            self._game_parser.ParseSection("ITEMS")
        # Items withou no effects are OK.
        self._game_parser.section_lines = ["water"]
        self._game_parser.ParseSection("ITEMS")

    def test_parse_map(self):
        self._game_parser.section_lines = [
            "dimensions:15:30 ",
            " player_start:0:14",
            "2:2:0:water:CO2",
            "2:3:3:water:",
            "0:2:2::CO2",
            ]
        self._game_parser.ParseSection("MAP")

        player = self._game_parser.player
        self.assertEqual(player.y_pos, 0)
        self.assertEqual(player.x_pos, 14)

        game_map = player.game_map
        self.assertEqual(game_map.height, 15)
        self.assertEqual(game_map.width, 30)
        room = game_map.GetRoom(2, 2)
        self.assertEqual(room.state, 0)
        self.assertEqual(room.contents, ["CO2", "water"])
        room = game_map.GetRoom(2, 3)
        self.assertEqual(room.state, 3)
        self.assertEqual(room.contents, ["water"])
        room = game_map.GetRoom(0, 2)
        self.assertEqual(room.state, 2)
        self.assertEqual(room.contents, ["CO2"])
        self.assertEqual(game_map.GetRoom(3, 3), None)
        self.assertEqual(game_map.GetRoom(15, 0), None)
        self.assertEqual(game_map.GetRoom(0, 30), None)

    def test_parse_aliases(self):
        self._game_parser.section_lines = ["go", "move", "run"]
        self._game_parser.ParseSection("ALIASES_MOVE")
        self._game_parser.section_lines = ["up", "forward"]
        self._game_parser.ParseSection("ALIASES_UP")
        self._game_parser.section_lines = ["stern", "south"]
        self._game_parser.ParseSection("ALIASES_DOWN")
        self._game_parser.section_lines = ["port", "left"]
        self._game_parser.ParseSection("ALIASES_LEFT")
        self._game_parser.section_lines = ["right", "starboard"]
        self._game_parser.ParseSection("ALIASES_RIGHT")
        self._game_parser.section_lines = ["use", "try"]
        self._game_parser.ParseSection("ALIASES_USE")
        self._game_parser.section_lines = ["add", "grab"]
        self._game_parser.ParseSection("ALIASES_ADD")
        self._game_parser.section_lines = ["drop", "discard", "throw away"]
        self._game_parser.ParseSection("ALIASES_DROP")
        self._game_parser.section_lines = ["look", "inspect", "examine"]
        self._game_parser.ParseSection("ALIASES_INSPECT")

        game_interface = self._game_parser.game_interface
        # Check these move aliases have registered and we can parse the commands
        # as they will be a method, not None.
        self.assertNotEqual(game_interface.LookupAction("go left")[0], None)
        self.assertNotEqual(game_interface.LookupAction("run up")[0], None)
        self.assertNotEqual(game_interface.LookupAction("move stern")[0], None)
        # These are move commands that are not understood.
        self.assertEqual(game_interface.LookupAction("move somewhere")[0], None)
        self.assertEqual(game_interface.LookupAction("fly left")[0], None)
        # Check these action alias and the resulting arguments.
        self.assertNotEqual(game_interface.LookupAction("USE baton")[0], None)
        self.assertEqual(game_interface.LookupAction("use baton")[1], "baton")
        self.assertNotEqual(game_interface.LookupAction("try baton")[0], None)
        self.assertEqual(game_interface.LookupAction("Grab big bat")[1],
                         "big bat")
        self.assertNotEqual(game_interface.LookupAction("Inspect.")[0], "")
        self.assertEqual(
            game_interface.LookupAction("drop Your glasses, now!")[1],
            "your glasses, now")
        # These action commands are not understood.
        self.assertEqual(game_interface.LookupAction("used somewhere")[0], None)
        self.assertEqual(game_interface.LookupAction("inspector")[0], None)


class FullTest(unittest.TestCase):

    def setUp(self):
        self._parser = my_game_parser.GameParser()

    def test_full(self):
        # Loading a file makes this not really a unit test per se, but I ran
        # out of time to try and get the in-memory file stuff working.
        self._parser.Parse("configs/iss_fire.game")
        player = self._parser.player
        game_interface = self._parser.game_interface
        self.assertEqual(
            game_interface.DebugInfo(),
            ["GAME: ISS Fire",
             ("EXPOSITION: Welcome SpaceX Re-supply Robot to the International"
              " Space Station!  Unfortunatley, there is a fire on the station."
              "  All the astronauts have evacuated; the station is abandond."
              "  I can help you save the station, but you need to move around"
              " and put out the fires."),
             ("NOUNS: room=section,"
              " up=bow, down=stern, left=port, right=starboard")])
        self.assertEqual(player.room_state_mapper.GetState(0), ["fine"])
        self.assertEqual(player.room_state_mapper.GetState(3),
                         ["electrical fire", "fabric fire"])
        self.assertEqual(player.item_mapper.GetItem("foam").UseItem(2), 1)
        self.assertEqual(player.item_mapper.GetItem("CO2").UseItem(3), 1)

        self.assertEqual(player.y_pos, 0)
        self.assertEqual(player.x_pos, 4)
        self.assertEqual(player.game_map.height, 10)
        self.assertEqual(player.game_map.width, 10)

        self.assertNotEqual(game_interface.LookupAction("go left")[0], None)
        self.assertNotEqual(game_interface.LookupAction("USE baton")[0], None)
        self.assertNotEqual(game_interface.LookupAction("Inspect.")[0], "")


if __name__ == "__main__":
    unittest.main()
