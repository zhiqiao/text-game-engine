# Generic imports.
import unittest

# Game specific imports.
import my_game_object


class TestGameObject(unittest.TestCase):

    def setUp(self):
        self.game_obj = my_game_object.GameObject()
        self.game_obj.name = "hammer"
        self.game_obj.reusable = True
        self.game_obj.AddStateChange(1, 0)
        self.game_obj.AddStateChange(2, 0)
        self.game_obj.AddStateChange(3, 1)

    def test_add_change(self):
        self.assertEqual(self.game_obj.DebugInfo(),
                         ["hammer can:",
                          "change 1 to 0",
                          "change 2 to 0",
                          "change 3 to 1",
                          "reusable: yes"])
        self.game_obj.reusable = False
        self.assertEqual(self.game_obj.DebugInfo(),
                         ["hammer can:",
                          "change 1 to 0",
                          "change 2 to 0",
                          "change 3 to 1",
                          "reusable: no"])

    def test_usage(self):
        self.assertEqual(self.game_obj.UseObject(1), 0)
        self.assertEqual(self.game_obj.UseObject(2), 0)
        self.assertEqual(self.game_obj.UseObject(3), 1)
        self.assertEqual(self.game_obj.UseObject(4), 4)


if __name__ == '__main__':
    unittest.main()
