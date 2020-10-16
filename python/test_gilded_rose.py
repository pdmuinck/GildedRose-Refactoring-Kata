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
        with the specified unit.
        """
        items = [NormalItem("foo", 1, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(0, items[0].quality)

    def test_expired_normal_item_degrades_faster(self):
        """
        This method tests a normal item to degrade faster when it is expired.
        """
        items = [NormalItem("foo", 0, 4)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(2, items[0].quality)
        self.assertEqual(-1, items[0].sell_in)

    def test_normal_item_cannot_have_negative_quality(self):
        """
        This method test that the NormalItem object doesn't go below 0 for
        it's quality field
        """
        items = [NormalItem("foo", 0, -5), NormalItem("foo", 0, 0)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(0, items[0].quality)
        self.assertEqual(0, items[1].quality)

    def test_aged_brie_item_increases_in_quality_the_older_it_gets(self):
        """
        Method that tests whether a durable item increases in quality the 
        older it gets.
        """
        items = [AgedBrieItem("foo", 1, 10), TicketItem("bar", 10, 10), TicketItem("pj", 4, 10), TicketItem("banana", 0, 10)]
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
        items = [NormalItem("foo", 10, more_than_bound), NormalItem("bar", 10, upper_bound)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(more_than_bound - 1, items[0].quality)
        self.assertLess(upper_bound - 1, items[0].quality)

    def test_legendary_item_has_fixed_quality_value_and_sell_value(self):
        """
        This method tests that the legendary items have a fixed amount of 
        quality.
        """
        items = [LegendaryItem("Sulfuras, Hand of Ragnaros", 10, 80), LegendaryItem("Sulfuras, Hand of Ragnaros", 10, 90)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEqual(80, items[0].quality)
        self.assertEqual(90, items[1].quality)
        self.assertEquals(10, items[0].sell_in)

    def test_conjured_item_degrades_two_times_faster_than_normal_item(self):
        items = [ConjuredItem("foo", 3, 4)]
        gided_rose = GildedRose(items)
        gided_rose.update_quality()
        self.assertEquals(2, items[0].quality)



if __name__ == '__main__':
    unittest.main()
