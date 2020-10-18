# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose
from items import Item, StockItem, DurableStockItem, DegradableStockItem, ConjuredStockItem, BackStageTicketItem

class GildedRoseTest(unittest.TestCase):
    """
    This class tests methods update_quality_v2() against update_quality() for
    backwards compatability and correctness.

    Assertions are done between the results of both methods.
    """
    def test_degradable_item_will_decrease_in_quality_when_sell_date_reaches(self):
        """
        This method will test an Item and a DegradableStockItem instance 
        for decreasing quality value when sell date reaches.
        """
        items_v1 = [Item("foo", 1, 1)]
        items_v2 = [DegradableStockItem("foo", 1, 1)]
        gilded_rose_v1 = GildedRose(items_v1)
        gilded_rose_v2 = GildedRose(items_v2)
        gilded_rose_v1.update_quality()
        gilded_rose_v2.update_quality_v2()
        # assert original code
        self.assertEqual(0, items_v1[0].sell_in)
        self.assertEqual(0, items_v1[0].quality)
        # compare v2 with original
        self._compare_versions(items_v1[0], items_v2[0]) 

    def test_degradable_item_when_sell_date_is_reached(self):
        """
        This method tests a normal item to degrade faster when it is expired.
        """
        items_v1 = [Item("foo", 0, 4)]
        items_v2 = [DegradableStockItem("foo", 0, 4)]
        gilded_rose_v1 = GildedRose(items_v1)
        gilded_rose_v1.update_quality()
        gilded_rose_v2 = GildedRose(items_v2)
        gilded_rose_v2.update_quality_v2()

        #assert original code
        self.assertEqual(2, items_v1[0].quality)
        self.assertEqual(-1, items_v1[0].sell_in)

        #assert V2
        self._compare_versions(items_v1[0], items_v2[0])

    def test_degradable_item_cannot_have_negative_quality(self):
        
        items_v1 = [Item("foo", 0, -5), Item("foo", 0, 0)]
        gided_rose = GildedRose(items_v1)
        gided_rose.update_quality()
        # assert original code
        self.assertEqual(-5, items_v1[0].quality)
        self.assertEqual(0, items_v1[1].quality)

    def test_aged_brie_item_increases_in_quality_the_older_it_gets(self):
        """
        Method that tests whether a durable item increases in quality the 
        older it gets.
        """
        items_v1 = [Item("Aged Brie", 1, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 4, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 0, 10)]
        gided_rose = GildedRose(items_v1)
        gided_rose.update_quality()
        self.assertEqual(11, items_v1[0].quality)
        self.assertEqual(13, items_v1[2].quality)
        self.assertEqual(12, items_v1[1].quality)
        self.assertEqual(0, items_v1[3].quality)
        

    def test_quality_value_never_increases_when_greater_or_equal_than(self, upper_bound= 50):
        """
        This method tests that the quality value never increases when it is 
        greater or equal than an upper bound.

        Args:
            upper_bound (int, optional): the maximum bound. Defaults to 50.
        """
        more_than_bound = upper_bound + 10
        items_v1 = [Item("foo", 10, more_than_bound), Item("bar", 10, upper_bound)]
        gided_rose = GildedRose(items_v1)
        gided_rose.update_quality()
        self.assertEqual(more_than_bound - 1, items_v1[0].quality)
        self.assertLess(upper_bound - 1, items_v1[0].quality)

    def test_legendary_item_has_fixed_quality_value_and_sell_value(self):
        """
        This method tests that the legendary items_v1 have a fixed amount of 
        quality.
        """
        items_v1 = [Item("Sulfuras, Hand of Ragnaros", 10, 80), Item("Sulfuras, Hand of Ragnaros", 10, 90)]
        gided_rose = GildedRose(items_v1)
        gided_rose.update_quality()
        self.assertEqual(80, items_v1[0].quality)
        self.assertEqual(90, items_v1[1].quality)
        self.assertEqual(10, items_v1[0].sell_in)

    def _compare_versions(self, item_v1, item_v2):
        self.assertEqual(item_v1.name, item_v2.name)
        self.assertEqual(item_v1.sell_in, item_v2.sell_in)
        self.assertEqual(item_v1.quality, item_v2.quality)



if __name__ == '__main__':
    unittest.main()
