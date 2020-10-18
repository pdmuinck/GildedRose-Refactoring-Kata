# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose
from items import Item, StockItem, AgeableStockItem, DurableStockItem, DegradableStockItem, ConjuredStockItem, BackStageTicketItem

class GildedRoseTest(unittest.TestCase):
    """
    This class tests about 7 features for both V1 and V2 versions of the api GildedRose:
    - degradable items should decrease in quality over time
    - degradable items should decrease in quality faster when the sell date it hit
    - degradable items cannot have a negative quality value
    - ageable items should increase in quality over time
    - ageable items should have a maximum quality value of 50
    - backstage passes should increase in value over time, with increments when selling date approaches
    - durable items cannot be modified
    """
    def test_update_quality_v1_deducts_quality_value_of_degradable_item(self):
        items = [Item("foo", 1, 1)]
        gilded_rose_v1 = GildedRose(items)
        gilded_rose_v1.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    def test_update_quality_v2_deducts_quality_value_of_degradable_item(self):
        items = [DegradableStockItem("foo", 1, 1)]
        gilded_rose_v2 = GildedRose(items)
        gilded_rose_v2.update_quality_v2()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
    
    def test_update_quality_v1_deducts_more_quality_of_degradable_item_when_sell_date_is_reached(self):
        items = [Item("foo", 0, 4)]
        gilded_rose_v1 = GildedRose(items)
        gilded_rose_v1.update_quality()
        self.assertEqual(2, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_update_quality_v2_deducts_more_quality_of_degradable_item_when_sell_date_is_reached(self):
        items = [DegradableStockItem("foo", 0, 4)]
        gilded_rose_v1 = GildedRose(items)
        gilded_rose_v1.update_quality_v2()
        self.assertEqual(2, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_update_quality_does_not_set_negative_quality_value(self):
        items = [Item("foo", 3, 0)]
        gilded_rose_v1 = GildedRose(items)
        gilded_rose_v1.update_quality()
        self.assertEqual(0, items[0].quality)

    def test_update_quality_v2_does_not_set_negative_quality_value(self):
        items = [DegradableStockItem("foo", 3, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality_v2()
        self.assertEqual(0, items[0].quality)
    
    def test_update_quality_increases_quality_of_ageable_items(self):
        items = [Item("Aged Brie", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(11, items[0].quality)

    def test_update_quality_increases_quality_of_ageable_items(self):
        items = [AgeableStockItem("foo", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality_v2()
        self.assertEqual(11, items[0].quality)

    def test_update_quality_increases_quality_backstage_tickets(self):
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 10, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 4, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(12, items[0].quality)
        self.assertEqual(13, items[1].quality)
        self.assertEqual(0, items[2].quality)
    
    def test_update_quality_v2_increases_quality_backstage_tickets(self):
        items = [BackStageTicketItem("foo", 10, 10), 
            BackStageTicketItem("bar", 4, 10), 
            BackStageTicketItem("pj", 0, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality_v2()
        self.assertEqual(12, items[0].quality)
        self.assertEqual(13, items[1].quality)
        self.assertEqual(0, items[2].quality)

    def test_update_quality_does_not_increase_quality_when_maximum_is_hit(self):
        items = [Item("Aged Brie", 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(50, items[0].quality)

    def test_update_quality_v2_does_not_increase_quality_when_maximum_is_hit(self):
        items = [AgeableStockItem("foo", 10, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality_v2()
        self.assertEqual(50, items[0].quality)
    
    def test_update_quality_v1_does_not_change_quality_of_durable_item(self):
        items = [Item("Sulfuras, Hand of Ragnaros", 10, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(10, items[0].sell_in)
    
    def test_update_quality_v2_does_not_change_quality_of_durable_item_(self):
        items = [DurableStockItem("Sulfuras, Hand of Ragnaros", 10, 80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality_v2()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(10, items[0].sell_in)
    
    def test_instantiate_stock_item_with_negative_quality_should_raise_exception(self):
        with self.assertRaises(Exception):
            StockItem("foo", 3, -20)
    
    def test_instantiate_item_with_negative_quality_should_work(self):
        item = Item("foo", 2, -20)
        self.assertEqual(-20, item.quality)
    
    def test_update_quality_v2_with_V1_item_should_raise_exception(self):
        gilded_rose = GildedRose([Item("foo", 1, 2)])
        with self.assertRaises(Exception):
            gilded_rose.update_quality_v2()

    def test_update_quality_v1_with_V2_items_should_raise_exception(self):
        gilded_rose = GildedRose([StockItem("foo", 1, 2)])
        with self.assertRaises(Exception):
            gilded_rose.update_quality()


if __name__ == '__main__':
    unittest.main()
