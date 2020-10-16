# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose
from items import Item, NormalItem, AgedBrieItem, LegendaryItem, ConjuredItem, TicketItem

class GildedRoseTest(unittest.TestCase):
    """
    This class tests methods update_quality_v2() against update_quality() for
    backwards compatability and correctness.

    Assertions are done between the results of both methods.
    """
    def test_at_the_end_of_each_day_sell_in_and_quality_decreases_for_normal_item(self):
        """
        This method will test whether sell_in and quality of Item is decreased
        when update_quality() is called.
        V2 version results are compared with original version results.
        """
        items = [Item("foo", 1, 1)]
        items_v2 = [NormalItem("foo", 1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose_v2 = GildedRose(items_v2)
        gilded_rose.update_quality()
        gilded_rose_v2.update_quality_v2()
        # test original code
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(0, items[0].quality)
        # compare v2 with original
        self._compare_versions(items[0], items_v2[0]) 

    def test_expired_normal_item_degrades_faster(self):
        """
        This method tests a normal item to degrade faster when it is expired.
        """
        items = [Item("foo", 0, 4)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(2, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_normal_item_cannot_have_negative_quality(self):
        """
        This method test that the NormalItem object doesn't go below 0 for
        it's quality field
        """
        items = [Item("foo", 0, -5), Item("foo", 0, 0)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(-5, items[0].quality)
        self.assertEqual(0, items[1].quality)

    def test_aged_brie_item_increases_in_quality_the_older_it_gets(self):
        """
        Method that tests whether a durable item increases in quality the 
        older it gets.
        """
        items = [Item("Aged Brie", 1, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 4, 10), 
            Item("Backstage passes to a TAFKAL80ETC concert", 0, 10)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(11, items[0].quality)
        self.assertEqual(13, items[2].quality)
        self.assertEqual(12, items[1].quality)
        self.assertEqual(0, items[3].quality)
        

    def test_quality_value_never_increases_when_greater_or_equal_than(self, upper_bound= 50):
        """
        This method tests that the quality value never increases when it is 
        greater or equal than an upper bound.

        Args:
            upper_bound (int, optional): the maximum bound. Defaults to 50.
        """
        more_than_bound = upper_bound + 10
        items = [Item("foo", 10, more_than_bound), Item("bar", 10, upper_bound)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(more_than_bound - 1, items[0].quality)
        self.assertLess(upper_bound - 1, items[0].quality)

    def test_legendary_item_has_fixed_quality_value_and_sell_value(self):
        """
        This method tests that the legendary items have a fixed amount of 
        quality.
        """
        items = [Item("Sulfuras, Hand of Ragnaros", 10, 80), Item("Sulfuras, Hand of Ragnaros", 10, 90)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(90, items[1].quality)
        self.assertEquals(10, items[0].sell_in)

    def _compare_versions(self, item_x, item_y):
        self.assertEqual(item_x.name, item_y.name)
        self.assertEqual(item_x.sell_in, item_y.sell_in)
        self.assertEqual(item_x.quality, item_y.quality)



if __name__ == '__main__':
    unittest.main()
