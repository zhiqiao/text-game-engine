import unittest

import my_game_utils


class TestUtils(unittest.TestCase):

    def test_remove_content(self):
        self.assertEqual(my_game_utils.RemoveContent([], None), None)
        self.assertEqual(my_game_utils.RemoveContent([], "A"), None)
        self.assertEqual(my_game_utils.RemoveContent(["B"], "A"), None)
        self.assertEqual(my_game_utils.RemoveContent(["B"], "B"), "B")
        self.assertEqual(my_game_utils.RemoveContent(["B", "A"], "B"), "B")
        self.assertEqual(my_game_utils.RemoveContent(["A", "A"], "B"), None)
        self.assertEqual(my_game_utils.RemoveContent(["A", "A"], "A"), "A")
        self.assertEqual(my_game_utils.RemoveContent(["A", "C"], "B"), None)
        self.assertEqual(my_game_utils.RemoveContent(["A", "B", "C"], "B"), "B")
        self.assertEqual(my_game_utils.RemoveContent(["A", "B", "C"], "D"), None)

    def test_display_contents(self):
        self.assertEqual(my_game_utils.GetContentsDisplay([]), [])
        self.assertEqual(my_game_utils.GetContentsDisplay(["A"]), ["1xA"])
        self.assertEqual(my_game_utils.GetContentsDisplay(["A", "A"]), ["2xA"])
        self.assertEqual(my_game_utils.GetContentsDisplay(["B", "A"]),
                         ["1xA", "1xB"])
        self.assertEqual(my_game_utils.GetContentsDisplay(["A", "B", "A", "C"]),
                         ["2xA", "1xB", "1xC"])
        self.assertEqual(
            my_game_utils.GetContentsDisplay(["A", "B", "A", "C", "C"]),
            ["2xA", "1xB", "2xC"])


if __name__ == '__main__':
    unittest.main()
