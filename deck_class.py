import random


class Deck:
    def __init__(self):
        self.draw_pile = list(range(0, 52))
        self.discards = []
        # self.in_play = [] #this might be unnecessary and is computationally intensive to keep up to date possibly?? maybe would be easier if dictionary?

    def shuffle(self):
        random.shuffle(self.draw_pile)

    def shuffle_in_discards(self):
        # shuffle discards, add draw pile to front of that list, make that the new draw pile, discards is empty.
        pass

    def deal(self, num_cards):
        # returns the cards delt
        if len(self.draw_pile) < num_cards:
            self.shuffle_in_discards()
        delt_cards = self.draw_pile[0:num_cards]
        self.draw_pile = self.draw_pile[num_cards:]
        # self.in_play.extend(delt_cards)
        return delt_cards
