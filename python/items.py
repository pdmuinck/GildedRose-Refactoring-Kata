class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

class NormalItem(Item):
    MAXIMUM_QUALITY = 50
    MINIMUM_QUALITY = 0
    UNIT = 1

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
        if(quality > self.MAXIMUM_QUALITY):
            self.quality = self.MAXIMUM_QUALITY
        if(quality < self.MINIMUM_QUALITY):
            self.quality = self.MINIMUM_QUALITY
    
    def update_sell_in(self):
        self.sell_in -= self.UNIT

    def update_quality(self):
        if(self.quality > 0):
            if(self._expired()):
                self.quality -= self.UNIT * 2
            else:
                self.quality -= self.UNIT

        
    def _expired(self):
        return self.sell_in < 0

class AgedBrieItem(NormalItem):

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
    
    def update_quality(self):
        self.quality += super().UNIT

class LegendaryItem(NormalItem):
    
    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
    
    def update_sell_in(self):
        """
        no decrease for legendary items
        """
    
    def update_quality(self):
        """
        no decrease for legendary items
        """

class TicketItem(NormalItem):

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)
    
    def update_quality(self):
        if(self.sell_in < 6 and self.sell_in >= 0):
            self.quality += 3
        elif(self.sell_in < 11 and self.sell_in > 5):
            self.quality += 2
        elif(self.sell_in < 0):
            self.quality = 0
        else:
            self.quality += 1

class ConjuredItem(NormalItem):

    def __init__(self, name, sell_in, quality):
        super().__init__(name, sell_in, quality)

    def update_quality(self):
        """
        Degrades twice as fast as a normal item
        """
        for x in range(super().UNIT * 2):
            super().update_quality()
