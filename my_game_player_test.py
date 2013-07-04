import unittest

import my_game_item
import my_game_map
import my_game_player
import my_game_room

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = my_game_player.Player()

    def test_properties(self):
        self.assertEqual(self.player.name, None)
        self.player.name = "test"
        self.assertEqual(self.player.name, "test")

        self.assertEqual(self.player.game_map, None)
        self.player.game_map = [[None]]
        self.assertEqual(self.player.game_map, [[None]])

        self.assertEqual(self.player.curr_room, None)
        self.player.curr_room = my_game_room.Room()
        self.assertNotEqual(self.player.curr_room, None)

        self.assertEqual(self.player.y_pos, None)
        self.player.y_pos = 8
        self.assertEqual(self.player.y_pos, 8)

        self.assertEqual(self.player.x_pos, None)
        self.player.x_pos = 8
        self.assertEqual(self.player.x_pos, 8)

        self.assertEqual(self.player.inventory, [])
        self.player.inventory = [1]
        self.assertEqual(self.player.inventory, [1])

        self.assertEqual(self.player.max_inventory_size, 0)
        self.player.max_inventory_size = 10
        self.assertEqual(self.player.max_inventory_size, 10)

        self.assertEqual(self.player.room_state_mapper, None)
        self.player.room_state_mapper = my_game_room.RoomStateMapper()
        self.assertNotEqual(self.player.room_state_mapper, None)

        self.assertEqual(self.player.item_mapper, None)
        self.player.item_mapper = my_game_item.ItemMapper()
        self.assertNotEqual(self.player.item_mapper, None)

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
        game_map.SetRoom(0, 0, "1")
        game_map.SetRoom(0, 1, "2")
        game_map.SetRoom(0, 2, "3")
        game_map.SetRoom(1, 1, "5")
        game_map.SetRoom(2, 0, "7")
        game_map.SetRoom(2, 1, "8")
        self.player.game_map = game_map
        self.player.y_pos = 0
        self.player.x_pos = 0
        self.player.item_mapper = my_game_item.ItemMapper()
        self.player.room_state_mapper = my_game_room.RoomStateMapper()
        self.assertTrue(self.player.Start())
        self.assertEqual(str(self.player.curr_room), "1")
        self.assertFalse(self.player.MoveUp())     # (0, 0)
        self.assertEqual(self.player.y_pos, 0)
        self.assertEqual(self.player.x_pos, 0)
        self.assertFalse(self.player.MoveDown())   # (0, 0)
        self.assertFalse(self.player.MoveLeft())   # (0, 0)
        self.assertTrue(self.player.MoveRight())   # (0, 1)
        self.assertEqual(self.player.y_pos, 0)
        self.assertEqual(self.player.x_pos, 1)
        self.assertTrue(self.player.MoveRight())   # (0, 2)
        self.assertEqual(self.player.y_pos, 0)
        self.assertEqual(self.player.x_pos, 2)
        self.assertFalse(self.player.MoveRight())  # (0, 2)
        self.assertTrue(self.player.MoveLeft())    # (0, 1)
        self.assertEqual(self.player.y_pos, 0)
        self.assertEqual(self.player.x_pos, 1)
        self.assertTrue(self.player.MoveDown())    # (1, 1)
        self.assertEqual(self.player.y_pos, 1)
        self.assertEqual(self.player.x_pos, 1)
        self.assertFalse(self.player.MoveLeft())   # (1, 1)
        self.assertFalse(self.player.MoveRight())  # (1, 1)
        self.assertTrue(self.player.MoveDown())    # (2, 1)
        self.assertTrue(self.player.MoveLeft())   # (2, 0)
        self.assertEqual(self.player.y_pos, 2)
        self.assertEqual(self.player.x_pos, 0)
        self.assertEqual(str(self.player.curr_room), "7")

    def test_minimal_map(self):
        game_map = my_game_map.GameMap()
        game_map.height = 1
        game_map.width = 1
        game_map.Initialize()
        game_map.SetRoom(0, 0, "1")
        self.player.game_map = game_map
        self.player.y_pos = 0
        self.player.x_pos = 0
        self.player.item_mapper = my_game_item.ItemMapper()
        self.player.room_state_mapper = my_game_room.RoomStateMapper()
        self.assertTrue(self.player.Start())

    def test_invalid_map(self):
        game_map = my_game_map.GameMap()
        game_map.height = 2
        game_map.width = 2
        game_map.Initialize()
        self.player.game_map = game_map
        self.player.y_pos = 0
        self.player.x_pos = 0
        # There are no valid rooms on the map.
        self.assertFalse(self.player.Start())

    def test_invalid_start(self):
        game_map = my_game_map.GameMap()
        game_map.height = 1
        game_map.width = 1
        game_map.Initialize()
        game_map.SetRoom(0, 0, "1")
        self.player.game_map = game_map
        self.player.y_pos = 1
        self.player.x_pos = 0
        self.assertFalse(self.player.Start())
        self.player.y_pos = 0
        self.player.x_pos = 1
        self.assertFalse(self.player.Start())

    def test_add_items(self):
        self.assertEqual(self.player.inventory, [])
        self.assertFalse(self.player.AddItem("A"))
        self.player.max_inventory_size = 1
        self.assertTrue(self.player.AddItem("A"))
        self.assertFalse(self.player.AddItem("B"))
        self.assertFalse(self.player.AddItem("A"))
        self.assertEqual(self.player.inventory, ["A"])
        self.player.max_inventory_size = 5
        self.assertTrue(self.player.AddItem("B"))
        self.assertTrue(self.player.AddItem("B"))
        self.assertTrue(self.player.AddItem("C"))
        self.assertTrue(self.player.AddItem("A"))
        self.assertFalse(self.player.AddItem("B"))
        self.assertEqual(self.player.inventory, ["A", "A", "B", "B", "C"])
        
    def test_drop_items(self):
        self.player.curr_room = my_game_room.Room()
        self.player.max_inventory_size = 5
        self.player.AddItem("A")
        self.player.AddItem("B")
        self.player.AddItem("A")
        self.player.AddItem("C")
        self.player.AddItem("A")
        self.assertEqual(self.player.inventory, ["A", "A", "A", "B", "C"])
        self.assertFalse(self.player.DropItem("D"))
        self.assertEqual(self.player.inventory, ["A", "A", "A", "B", "C"])
        self.assertTrue(self.player.DropItem("A"))
        self.assertEqual(self.player.inventory, ["A", "A", "B", "C"])
        self.assertTrue(self.player.DropItem("A"))
        self.assertTrue(self.player.DropItem("A"))
        self.assertFalse(self.player.DropItem("A"))
        self.assertEqual(self.player.inventory, ["B", "C"])
        self.assertTrue(self.player.AddItem("C"))
        self.assertTrue(self.player.AddItem("C"))
        self.assertTrue(self.player.AddItem("C"))
        self.assertFalse(self.player.AddItem("C"))
        self.assertEqual(self.player.inventory, ["B", "C", "C", "C", "C"])
        self.player.max_inventory_size = 4
        self.assertEqual(self.player.inventory, ["B", "C", "C", "C", "C"])
        self.assertTrue(self.player.DropItem("B"))
        self.assertEqual(self.player.inventory, ["C", "C", "C", "C"])
        self.assertFalse(self.player.AddItem("B"))
        self.assertTrue(self.player.DropItem("C"))
        self.assertTrue(self.player.DropItem("C"))
        self.assertTrue(self.player.DropItem("C"))
        self.assertTrue(self.player.DropItem("C"))
        self.assertFalse(self.player.DropItem("C"))
        self.assertEqual(self.player.inventory, [])

    def test_use_item(self):
        self.player.curr_room = my_game_room.Room()
        self.player.curr_room.state = 0
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

        self.player.item_mapper = item_mapper
        self.player.max_inventory_size = 4
        self.player.AddItem("A")
        self.player.AddItem("B")
        self.player.AddItem("C")
        self.player.AddItem("E")
        self.assertEqual(self.player.inventory, ["A", "B", "C", "E"])

        # No item in inventory.
        self.assertFalse(self.player.UseItem("D"))
        
        # C is reusable, but does nothing.
        self.assertFalse(self.player.UseItem("C"))
        self.assertEqual(self.player.inventory, ["A", "B", "C", "E"])

        # B is reusable, but does nothing in state 0.
        self.assertFalse(self.player.UseItem("B"))
        self.assertEqual(self.player.inventory, ["A", "B", "C", "E"])

        # E is not reusable and does nothing in state 0.
        self.assertFalse(self.player.UseItem("E"))
        self.assertEqual(self.player.inventory, ["A", "B", "C"])

        self.player.curr_room.state = 1
        # A is reusable and moves the room from state 1 to 0.
        self.assertTrue(self.player.UseItem("A"))
        self.assertEqual(self.player.inventory, ["A", "B", "C"])
        self.assertEqual(self.player.curr_room.state, 0)

        self.player.curr_room.state = 3
        # B is reusable and moves the room from state 3 to 1.
        self.assertTrue(self.player.UseItem("B"))
        self.assertEqual(self.player.inventory, ["A", "B", "C"])
        # A is reusable and moves the room from state 1 to 0. 
        self.assertEqual(self.player.curr_room.state, 1)
        self.assertTrue(self.player.UseItem("A"))
        self.assertEqual(self.player.inventory, ["A", "B", "C"])
        self.assertEqual(self.player.curr_room.state, 0)

    def test_inspect(self):
        state_mapper = my_game_room.RoomStateMapper()
        state_mapper.AddState(1, ["cold", "wet", "calm"])
        self.player.room_state_mapper = state_mapper
        self.player.curr_room = my_game_room.Room()
        self.assertEqual(self.player.Inspect(), {"room": [], "inventory": []})
        self.player.curr_room.state = 1
        self.assertEqual(self.player.Inspect(),
                         {"room": ["cold", "wet", "calm"], "inventory": []})
        self.player.max_inventory_size = 5
        self.player.AddItem("A")
        self.player.AddItem("B")
        self.player.AddItem("A")
        self.player.AddItem("C")
        self.player.AddItem("A")
        self.assertEqual(self.player.Inspect(),
                         {'room': ['cold', 'wet', 'calm'],
                          'inventory': ['3xA', '1xB', '1xC']
                         })

if __name__ == "__main__":
    unittest.main()
