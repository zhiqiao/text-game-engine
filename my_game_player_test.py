import unittest

import my_game_item
import my_game_map
import my_game_player
import my_game_room

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self._player = my_game_player.Player()
        self._player.curr_room = my_game_room.Room()
        self._player.curr_room.state = 0
        self._player.curr_room.contents = [
            "A", "A", "A", "B", "B", "B", "B", "C", "C", "C", "C"]

    def test_properties(self):
        self.assertEqual(self._player.y_pos, None)
        self._player.y_pos = 8
        self.assertEqual(self._player.y_pos, 8)

        self.assertEqual(self._player.x_pos, None)
        self._player.x_pos = 8
        self.assertEqual(self._player.x_pos, 8)

        self.assertEqual(self._player.inventory, [])
        self._player.inventory = [1]
        self.assertEqual(self._player.inventory, [1])

        self.assertEqual(self._player.max_inventory_size, 0)
        self._player.max_inventory_size = 10
        self.assertEqual(self._player.max_inventory_size, 10)

        # These three objects are associated to the player and thus instantiated
        # in init()
        self.assertNotEqual(self._player.game_map, None)
        self.assertNotEqual(self._player.room_state_mapper, None)
        self.assertNotEqual(self._player.item_mapper, None)

    def test_movement(self):
        game_map = my_game_map.GameMap()
        game_map.height = 3
        game_map.width = 3
        game_map.Initialize()
        # +---+
        # |123|
        # |#5#|
        # |78#|
        # +---+
        room1 = my_game_room.Room()
        room1.state = 1
        room2 = my_game_room.Room()
        room2.state = 2
        room3 = my_game_room.Room()
        room3.state = 3
        room5 = my_game_room.Room()
        room5.state = 5
        room7 = my_game_room.Room()
        room7.state = 7
        room8 = my_game_room.Room()
        room8.state = 8
        game_map.SetRoom(0, 0, room1)
        game_map.SetRoom(0, 1, room2)
        game_map.SetRoom(0, 2, room3)
        game_map.SetRoom(1, 1, room5)
        game_map.SetRoom(2, 0, room7)
        game_map.SetRoom(2, 1, room8)
        self._player.game_map = game_map
        self._player.y_pos = 0
        self._player.x_pos = 0
        self._player.item_mapper = my_game_item.ItemMapper()
        self._player.room_state_mapper = my_game_room.RoomStateMapper()
        self.assertTrue(self._player.Start())
        self.assertEqual(self._player.curr_room.state, 1)
        self.assertFalse(self._player.MoveUp()[0])     # (0, 0)
        self.assertEqual(self._player.y_pos, 0)
        self.assertEqual(self._player.x_pos, 0)
        self.assertFalse(self._player.MoveDown()[0])   # (0, 0)
        self.assertFalse(self._player.MoveLeft()[0])   # (0, 0)
        self.assertTrue(self._player.MoveRight()[0])   # (0, 1)
        self.assertEqual(self._player.y_pos, 0)
        self.assertEqual(self._player.x_pos, 1)
        self.assertTrue(self._player.MoveRight()[0])   # (0, 2)
        self.assertEqual(self._player.y_pos, 0)
        self.assertEqual(self._player.x_pos, 2)
        self.assertFalse(self._player.MoveRight()[0])  # (0, 2)
        self.assertTrue(self._player.MoveLeft()[0])    # (0, 1)
        self.assertEqual(self._player.y_pos, 0)
        self.assertEqual(self._player.x_pos, 1)
        self.assertTrue(self._player.MoveDown()[0])    # (1, 1)
        self.assertEqual(self._player.y_pos, 1)
        self.assertEqual(self._player.x_pos, 1)
        self.assertFalse(self._player.MoveLeft()[0])   # (1, 1)
        self.assertFalse(self._player.MoveRight()[0])  # (1, 1)
        self.assertTrue(self._player.MoveDown()[0])    # (2, 1)
        self.assertTrue(self._player.MoveLeft()[0])   # (2, 0)
        self.assertEqual(self._player.y_pos, 2)
        self.assertEqual(self._player.x_pos, 0)
        self.assertEqual(self._player.curr_room.state, 7)

    def test_minimal_map(self):
        game_map = my_game_map.GameMap()
        game_map.height = 1
        game_map.width = 1
        game_map.Initialize()
        game_map.SetRoom(0, 0, "1")
        self._player.game_map = game_map
        self._player.y_pos = 0
        self._player.x_pos = 0
        self._player.item_mapper = my_game_item.ItemMapper()
        self._player.room_state_mapper = my_game_room.RoomStateMapper()
        self.assertTrue(self._player.Start())

    def test_invalid_map(self):
        game_map = my_game_map.GameMap()
        game_map.height = 2
        game_map.width = 2
        game_map.Initialize()
        self._player.game_map = game_map
        self._player.y_pos = 0
        self._player.x_pos = 0
        # There are no valid rooms on the map.
        self.assertFalse(self._player.Start())

    def test_invalid_start(self):
        game_map = my_game_map.GameMap()
        game_map.height = 1
        game_map.width = 1
        game_map.Initialize()
        game_map.SetRoom(0, 0, "1")
        self._player.game_map = game_map
        self._player.y_pos = 1
        self._player.x_pos = 0
        self.assertFalse(self._player.Start())
        self._player.y_pos = 0
        self._player.x_pos = 1
        self.assertFalse(self._player.Start())

    def test_add_items(self):
        self.assertEqual(self._player.inventory, [])
        self.assertFalse(self._player.AddItem("A")[0])
        self._player.max_inventory_size = 1
        self.assertTrue(self._player.AddItem("A")[0])
        self.assertFalse(self._player.AddItem("B")[0])
        self.assertFalse(self._player.AddItem("A")[0])
        self.assertEqual(self._player.inventory, ["A"])
        self._player.max_inventory_size = 5
        self.assertTrue(self._player.AddItem("B")[0])
        self.assertTrue(self._player.AddItem("B")[0])
        self.assertTrue(self._player.AddItem("C")[0])
        self.assertTrue(self._player.AddItem("A")[0])
        self.assertFalse(self._player.AddItem("B")[0])
        self.assertEqual(self._player.inventory, ["A", "A", "B", "B", "C"])
        
    def test_drop_items(self):
        self._player.max_inventory_size = 5
        self._player.AddItem("A")
        self._player.AddItem("B")
        self._player.AddItem("A")
        self._player.AddItem("C")
        self._player.AddItem("A")
        self.assertEqual(self._player.inventory, ["A", "A", "A", "B", "C"])
        self.assertFalse(self._player.DropItem("D")[0])
        self.assertEqual(self._player.inventory, ["A", "A", "A", "B", "C"])
        self.assertTrue(self._player.DropItem("A")[0])
        self.assertEqual(self._player.inventory, ["A", "A", "B", "C"])
        self.assertTrue(self._player.DropItem("A")[0])
        self.assertTrue(self._player.DropItem("A")[0])
        self.assertFalse(self._player.DropItem("A")[0])
        self.assertEqual(self._player.inventory, ["B", "C"])
        self.assertTrue(self._player.AddItem("C")[0])
        self.assertTrue(self._player.AddItem("C")[0])
        self.assertTrue(self._player.AddItem("C")[0])
        self.assertFalse(self._player.AddItem("C")[0])
        self.assertEqual(self._player.inventory, ["B", "C", "C", "C", "C"])
        self._player.max_inventory_size = 4
        self.assertEqual(self._player.inventory, ["B", "C", "C", "C", "C"])
        self.assertTrue(self._player.DropItem("B")[0])
        self.assertEqual(self._player.inventory, ["C", "C", "C", "C"])
        self.assertFalse(self._player.AddItem("B")[0])
        self.assertTrue(self._player.DropItem("C")[0])
        self.assertTrue(self._player.DropItem("C")[0])
        self.assertTrue(self._player.DropItem("C")[0])
        self.assertTrue(self._player.DropItem("C")[0])
        self.assertFalse(self._player.DropItem("C")[0])
        self.assertEqual(self._player.inventory, [])

    def test_use_item(self):
        self._player.curr_room.AddContent("E")
        item_mapper = my_game_item.ItemMapper()

        item_a = my_game_item.GameItem()
        item_a.AddStateChange(1, 0)
        item_a.reusable = True
        item_mapper.AddItem("A", item_a)

        item_b = my_game_item.GameItem()
        item_b.AddStateChange(2, 0)
        item_b.AddStateChange(3, 1)
        item_b.reusable = True
        item_mapper.AddItem("B", item_b)

        item_c = my_game_item.GameItem()
        item_c.reusable = True
        item_mapper.AddItem("C", item_c)

        item_d = my_game_item.GameItem()
        item_mapper.AddItem("C", item_d)

        item_e = my_game_item.GameItem()
        item_e.AddStateChange(1, 0)
        item_e.reusable = False
        item_mapper.AddItem("E", item_e)

        self._player.item_mapper = item_mapper
        self._player.max_inventory_size = 4
        self._player.AddItem("A")
        self._player.AddItem("B")
        self._player.AddItem("C")
        self._player.AddItem("E")
        self.assertEqual(self._player.inventory, ["A", "B", "C", "E"])

        # No item in inventory.
        self.assertFalse(self._player.UseItem("D")[0])
        
        # C is reusable, but does nothing.
        self.assertFalse(self._player.UseItem("C")[0])
        self.assertEqual(self._player.inventory, ["A", "B", "C", "E"])

        # B is reusable, but does nothing in state 0.
        self.assertFalse(self._player.UseItem("B")[0])
        self.assertEqual(self._player.inventory, ["A", "B", "C", "E"])

        # E is not reusable and does nothing in state 0.
        self.assertFalse(self._player.UseItem("E")[0])
        self.assertEqual(self._player.inventory, ["A", "B", "C"])

        self._player.curr_room.state = 1
        # A is reusable and moves the room from state 1 to 0.
        self.assertTrue(self._player.UseItem("A")[0])
        self.assertEqual(self._player.inventory, ["A", "B", "C"])
        self.assertEqual(self._player.curr_room.state, 0)

        self._player.curr_room.state = 3
        # B is reusable and moves the room from state 3 to 1.
        self.assertTrue(self._player.UseItem("B")[0])
        self.assertEqual(self._player.inventory, ["A", "B", "C"])
        # A is reusable and moves the room from state 1 to 0. 
        self.assertEqual(self._player.curr_room.state, 1)
        self.assertTrue(self._player.UseItem("A")[0])
        self.assertEqual(self._player.inventory, ["A", "B", "C"])
        self.assertEqual(self._player.curr_room.state, 0)

    def test_inspect(self):
        state_mapper = my_game_room.RoomStateMapper()
        self._player.room_state_mapper = state_mapper
        self.assertEqual(
            self._player.Inspect()[1],
            ("The room is [].  There are [3xA, 4xB, 4xC]."
             "  You currently have []."))
        state_mapper.AddState(0, ["cold", "wet", "calm"])
        self.assertEqual(
            self._player.Inspect()[1],
            ("The room is [cold, wet, calm].  There are [3xA, 4xB, 4xC]."
             "  You currently have []."))
        self._player.max_inventory_size = 5
        self._player.AddItem("A")
        self._player.AddItem("B")
        self._player.AddItem("A")
        self._player.AddItem("C")
        self._player.AddItem("A")
        self.assertEqual(
            self._player.Inspect()[1],
            ("The room is [cold, wet, calm].  There are [3xB, 3xC]."
             "  You currently have [3xA, 1xB, 1xC]."))


if __name__ == "__main__":
    unittest.main()
