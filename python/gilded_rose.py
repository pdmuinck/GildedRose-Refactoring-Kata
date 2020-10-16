# -*- coding: utf-8 -*-

class GildedRose(object):
    """
    This class contains two methods: update_quality and update_quality_v2.
    The latter method is backwards compatible with update_quality and contains
    some fixes and a new feature: it can handle a conjured item. 

    update_quality simply updates the quality of items and serves a list of Item 
    objects.

    update_quality_v2 does the same thing but provides an implementation to process
    subclasses from Item like GenericItem, TicketItem, AgedBrieItem, LegendaryItem
    and ConjuredItem.
    """

    def __init__(self, items):
        self.items = items
    
    
    def update_quality_v2(self):
        for item in self.items:
            item.update_sell_in()
            item.update_quality()


    def update_quality(self):
        for item in self.items:
            if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                    if item.quality > 0:
                        if item.name != "Sulfuras, Hand of Ragnaros":
                            item.quality = item.quality - 1
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            if item.name != "Sulfuras, Hand of Ragnaros":
                                item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1