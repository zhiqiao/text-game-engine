# Generic imports.
import unittest

# Game specific imports.
import my_game_room


class TestGameRoom(unittest.TestCase):

    def setUp(self):
        self.game_room = my_game_room.GameRoom()

    def test_state(self):
        self.game_room.state = 0
        self.assertEqual(self.game_room.state, 0)
        self.game_room.state = 1
        self.assertEqual(self.game_room.state, 1)
        self.game_room.state = 1
        self.assertEqual(self.game_room.state, 1)

    def test_add_content(self):
        self.game_room.state = 0
        self.game_room.AddContent("A")
        self.game_room.AddContent("A")
        self.game_room.AddContent("C")
        self.game_room.AddContent("A")
        self.game_room.AddContent("B")
        self.assertEqual(self.game_room.contents, ["A", "A", "A", "B", "C"])

    def test_remove_content(self):
        self.game_room.state = 0
        self.game_room.AddContent("C")
        self.game_room.AddContent("A")
        self.game_room.AddContent("B")
        self.game_room.AddContent("A")
        self.game_room.AddContent("B")
        self.game_room.AddContent("A")
        self.assertEqual(self.game_room.contents,
                         ["A", "A", "A", "B", "B", "C"])

        self.assertEqual(self.game_room.RemoveContent("A"), "A")
        self.assertEqual(self.game_room.contents, ["A", "A", "B", "B", "C"])

        self.assertEqual(self.game_room.RemoveContent("C"), "C")
        self.assertEqual(self.game_room.RemoveContent("C"), None)
        self.assertEqual(self.game_room.contents, ["A", "A", "B", "B"])

        self.assertEqual(self.game_room.RemoveContent("B"), "B")
        self.assertEqual(self.game_room.contents, ["A", "A", "B"])

        self.assertEqual(self.game_room.RemoveContent("A"), "A")
        self.assertEqual(self.game_room.RemoveContent("A"), "A")
        self.assertEqual(self.game_room.RemoveContent("A"), None)
        self.assertEqual(self.game_room.contents, ["B"])
        self.game_room.AddContent("A")
        self.assertEqual(self.game_room.contents, ["A", "B"])

    def test_display_content(self):
        self.game_room.state = 0
        self.game_room.AddContent("C")
        self.assertEqual(self.game_room.GetContentsDisplay(), ["1xC"])
        self.game_room.AddContent("A")
        self.assertEqual(self.game_room.GetContentsDisplay(), ["1xA", "1xC"])
        self.game_room.AddContent("B")
        self.assertEqual(self.game_room.GetContentsDisplay(),
                         ["1xA", "1xB", "1xC"])
        self.game_room.AddContent("A")
        self.assertEqual(self.game_room.GetContentsDisplay(),
                         ["2xA", "1xB", "1xC"])
        self.game_room.AddContent("B")
        self.assertEqual(self.game_room.GetContentsDisplay(),
                         ["2xA", "2xB", "1xC"])
        self.game_room.AddContent("A")
        self.assertEqual(self.game_room.GetContentsDisplay(),
                         ["3xA", "2xB", "1xC"])
        self.assertEqual(self.game_room.DebugInfo(),
                         ["STATE: 0", "CONTENTS: [3xA, 2xB, 1xC]"])
        self.assertEqual(self.game_room.RemoveContent("C"), "C")
        self.assertEqual(self.game_room.RemoveContent("C"), None)
        self.assertEqual(self.game_room.GetContentsDisplay(), ["3xA", "2xB"])
        self.assertEqual(self.game_room.RemoveContent("A"), "A")
        self.assertEqual(self.game_room.RemoveContent("A"), "A")
        self.assertEqual(self.game_room.RemoveContent("A"), "A")
        self.assertEqual(self.game_room.RemoveContent("A"), None)
        self.assertEqual(self.game_room.GetContentsDisplay(), ["2xB"])
        self.assertEqual(self.game_room.RemoveContent("B"), "B")
        self.assertEqual(self.game_room.RemoveContent("B"), "B")
        self.assertEqual(self.game_room.GetContentsDisplay(), [])
        self.assertEqual(self.game_room.DebugInfo(),
                         ["STATE: 0", "CONTENTS: []"])


class TestRoomState(unittest.TestCase):
    pass


class TestRoomStateMapper(unittest.TestCase):

    def setUp(self):
        self.room_states = my_game_room.RoomStateMapper()

    def test_add_state(self):
        self.room_states.AddState(0, "Everything's fine.")
        self.assertEqual(len(self.room_states.all_states), 1)
        self.room_states.AddState(1, "Room is on fire!")
        self.assertEqual(len(self.room_states.all_states), 2)
        self.room_states.AddState(0, "Everything's OK!")
        self.assertEqual(len(self.room_states.all_states), 2)

    def test_get_state(self):
        self.room_states.AddState(0, "Everything's fine.")
        self.room_states.AddState(1, "Room is on fire!")
        self.room_states.AddState(0, "Everything's OK!")
        self.assertEqual(self.room_states.GetState(0), "Everything's OK!")
        self.assertEqual(self.room_states.GetState(1), "Room is on fire!")


if __name__ == '__main__':
    unittest.main()
