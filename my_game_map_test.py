# Generic imports.
import unittest

# Game specific imports.
import my_game_map


class TestGameMap(unittest.TestCase):
    def setUp(self):
        self.game_map = my_game_map.GameMap()

    def test_default_properties(self):
        # Assert that all expected properties are present after instantiation.
        self.assertEquals(self.game_map.height, None)
        self.assertEquals(self.game_map.width, None)
        self.assertEquals(self.game_map.game_map, None)

    def test_setting_properties(self):
        # Assert that all settable properties can be set.
        self.game_map.height = 10
        self.game_map.width = 10
        self.assertEquals(self.game_map.height, 10)
        self.assertEquals(self.game_map.width, 10)

        # You should not be able to set the game map.
        with self.assertRaises(AttributeError):
            self.game_map.game_map = [[None]]

        # You should not be able to set invalid dimensions.
        with self.assertRaises(AssertionError):
            self.game_map.height = 0
        with self.assertRaises(AssertionError):
            self.game_map.height = -1
        with self.assertRaises(AssertionError):
            self.game_map.width = 0
        with self.assertRaises(AssertionError):
            self.game_map.width = -1

    def test_initialize(self):
        with self.assertRaises(AssertionError):
            self.game_map.Initialize()
        self.game_map.height = 10
        self.game_map.width = 10
        self.game_map.Initialize()
        self.assertEqual(len(self.game_map.game_map), 10)
        for row in self.game_map.game_map:
            self.assertEqual(len(row), 10)

    def test_setting_and_getting_rooms(self):
        self.game_map.height = 10
        self.game_map.width = 8
        self.game_map.Initialize()

        with self.assertRaises(AssertionError):
            self.game_map.SetRoom(-1, 0, "Test")
        with self.assertRaises(AssertionError):
            self.game_map.SetRoom(0, -1, "Test")
        with self.assertRaises(AssertionError):
            self.game_map.SetRoom(10, 0, "Test")
        with self.assertRaises(AssertionError):
            self.game_map.SetRoom(0, 10, "Test")

        self.assertEqual(self.game_map.SetRoom(0, 0, "T"), "T")
        self.assertEqual(self.game_map.SetRoom(0, 7, "E"), "E")
        self.assertEqual(self.game_map.SetRoom(9, 0, "S"), "S")
        self.assertEqual(self.game_map.SetRoom(9, 7, "T"), "T")

        self.assertEqual(self.game_map.GetRoom(9, 0), "S")
        self.assertEqual(self.game_map.GetRoom(9, 7), "T")
        self.assertEqual(self.game_map.GetRoom(9, 1), None)
        self.assertEqual(self.game_map.GetRoom(5, 5), None)

        output = self.game_map.DebugInfo()
        self.assertEqual(output[0], "T######E")
        self.assertEqual(output[9], "S######T")


if __name__ == '__main__':
    unittest.main()
