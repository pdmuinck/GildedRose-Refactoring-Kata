from enum import Enum

"""
This module defines classes related to stock items at gilded rose.

We have the original Item class with fields name, sell_in and quality.

Next we have a new StockItem class that holds fields name, item_type, sell_in
and quality.
"""

UNIT_OF_DAILY_DEGRADATION = 1
UNIT_OF_DAILY_IMPROVEMENT = 1
MAXIMUM_QUALITY = 50
MINIMUM_QUALITY = 0

class Item:
    """
    The original class, maintained by a goblin, do not alter this class or he
    gets angry.
    """
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class StockItem:
    """
    This class represents an item in stock for gilded rose. 
    This class is used in the V2 version of the API.
    Fields: name, sell_in, quality
    StockItem cannot be instantiated with negative quality value, exception is
    raised.
    """
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        if(quality < 0): raise Exception("Cannot create a stock item with "
        + "negative quality.")
        self.quality = quality

    def change_sell_in(self):
        """
        Decreases the sell_in field with one.
        """
        self.sell_in -= 1
    
    def change_quality(self):
        pass

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class DegradableStockItem(StockItem):
    """
    This class is meant to identify stock items that degrade over time.
    Simply put the quality value will decrease every day.
    By default the degradation multiplier is 1.
    """
    def __init__(self, name, sell_in, quality, degradation_multiplier=1):
        super().__init__(name, sell_in, quality)
        self.degradation_multiplier = degradation_multiplier
    
    def change_quality(self):
        """
        Subtracts the UNIT_OF_DAILY_DEGRADATION member from the quality field.
        If the sell date is expires, the item degrades twice as fast.
        The quality of an item is never negative.
        Applies the degradation multiplier.
        """
        if(self.quality > MINIMUM_QUALITY and self.sell_date_expired()):
            self.quality -= 2 * self.degradation_multiplier * UNIT_OF_DAILY_DEGRADATION
        elif(self.quality > MINIMUM_QUALITY):
            self.quality -= self.degradation_multiplier * UNIT_OF_DAILY_DEGRADATION
    
    def sell_date_expired(self):
        return self.sell_in < 0

class AgeableStockItem(StockItem):
    """
    Instances of this class will get better over time.
    The quality value will increase every day.
    """
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
    
    def change_quality(self):
        """
        Increases the quality field with the UNIT_OF_DAILY_IMPROVEMENT field.
        The quality value cannot be higher than the MAXIMUM_QUALITY member.
        """
        if(self.quality < MAXIMUM_QUALITY):
            self.quality += UNIT_OF_DAILY_IMPROVEMENT

class DurableStockItem(StockItem):
    """
    Describes an item of which the quality doesn't change.
    """
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def change_sell_in(self):
        """
        sell_in will not change for durable items
        """
        pass

    
    def change_quality(self):
        """
        Quality will not change for durable times.
        """
        pass

class ConjuredStockItem(DegradableStockItem):
    """
    Conjured stock items degrade twice as fast.
    So the degradation_multiplier is set to 2.
    """
    def __init__(self, name, sell_in, quality, degradation_multiplier):
        super().__init__(name, sell_in, quality, 2)

class BackStageTicketItem(AgeableStockItem):
    """
    Special stock item that increases in quality value but also drops to zero when sell
    date is reached.
    """
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def change_quality(self):
        """
        The quality increases when sell date progresses.
        When sell date is hit, the quality is set to zero.
        """
        if(self.sell_in > 5 and self.sell_in < 11):
            self.quality += 2
        elif(self.sell_in < 6 and self.sell_in >= 0):
            self.quality += 3
        elif(self.sell_in < 0):
            self.quality = 0
        else:
            self.quality += 1
