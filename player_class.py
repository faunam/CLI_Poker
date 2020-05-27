class Player:
    def __init__(self, id=0):
        self.id = id
        self.hand = []
        self.active = True  # this may not be useful? idk
        self.chips = 20
        self.current_bet = 0

    def discard(self, discards):
        d_set = set(discards)
        self.hand = [card for card in self.hand if card not in d_set]

    def bet(self, num_chips):
        # returns the amount by which the player increased their bet, so the pot is modified accordingly
        difference = num_chips - self.current_bet
        self.chips = self.chips - difference
        if self.chips < 0:
            self.active = False
            print("Player " + str(self.id) +
                  ", you ran out of chips. you're out of the game!")
        self.current_bet = num_chips
        return difference

    def print_hand(self):
        suits = 'HCDS'
        royals = 'JQKA'
        representations = []
        for card in self.hand:
            number = card % 13 + 2
            suit = suits[card//13]
            if number > 10:
                representations.append(royals[number-11] + suit)
            else:
                representations.append(str(number) + suit)
        print("    ,    ".join(representations))
