# Generic imports.
import unittest

# Game specific imports.
import my_game_item


class TestItemMapper(unittest.TestCase):

    def setUp(self):
        self.item_mapper = my_game_item.ItemMapper()

    def test_default(self):
        self.assertEqual(self.item_mapper.all_items, {})
        # GameItem.__eq__ should allow this default item to be equal.
        self.assertEqual(self.item_mapper.GetItem("A"),
                         my_game_item.GameItem())

    def test_item_ownership(self):
        item = my_game_item.GameItem()
        item.AddStateChange(1, 0)
        self.item_mapper.AddItem("A", item)
        item.AddStateChange(3, 2)
        stored_item = self.item_mapper.GetItem("A")
        # Test this is not a default item.
        self.assertNotEqual(stored_item, my_game_item.GameItem())
        self.assertNotEqual(stored_item, item)
        self.assertEqual(item.UseItem(3), 2)
        self.assertEqual(stored_item.UseItem(3), 3)

    def test_add_item(self):
        item_1 = my_game_item.GameItem()
        item_1.AddStateChange(1, 0)
        self.item_mapper.AddItem("A", item_1)
        item_2 = my_game_item.GameItem()
        item_2.AddStateChange(2, 0)
        self.item_mapper.AddItem("A", item_2)
        item_3 = my_game_item.GameItem()
        item_3.AddStateChange(3, 0)
        self.item_mapper.AddItem("B", item_3)

        stored_item = self.item_mapper.GetItem("A")
        self.assertEqual(stored_item.UseItem(1), 1)
        self.assertEqual(stored_item.UseItem(2), 0)

        stored_item = self.item_mapper.GetItem("B")
        self.assertEqual(stored_item.UseItem(3), 0)
        self.assertEqual(stored_item.UseItem(2), 2)

        stored_item = self.item_mapper.GetItem("C")
        self.assertEqual(stored_item.UseItem(3), 3)


class TestGameItem(unittest.TestCase):

    def setUp(self):
        self.game_item = my_game_item.GameItem()
        self.game_item.name = "hammer"
        self.game_item.reusable = True
        self.game_item.AddStateChange(1, 0)
        self.game_item.AddStateChange(2, 0)
        self.game_item.AddStateChange(3, 1)

    def test_add_change(self):
        self.assertEqual(self.game_item.DebugInfo(),
                         ["hammer can:",
                          "change 1 to 0",
                          "change 2 to 0",
                          "change 3 to 1",
                          "reusable: yes"])
        self.game_item.reusable = False
        self.assertEqual(self.game_item.DebugInfo(),
                         ["hammer can:",
                          "change 1 to 0",
                          "change 2 to 0",
                          "change 3 to 1",
                          "reusable: no"])

    def test_usage(self):
        self.assertEqual(self.game_item.UseItem(1), 0)
        self.assertEqual(self.game_item.UseItem(2), 0)
        self.assertEqual(self.game_item.UseItem(3), 1)
        self.assertEqual(self.game_item.UseItem(4), 4)


if __name__ == '__main__':
    unittest.main()
