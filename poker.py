# class for the deck - features like discards, cards in play, draw_pile
# player class - cards in hand, combinations (maybe it automatically plays the highest combo you have), in_game (eg have folded)
# game class -- high score for that session, bets, quit?, deal function

# focus on first round -- each player get 5 random cards, discard up to 5, get all new cards (from a pile not containing your discards or cards in hand)
# next, add multiple player functionality
# scoring function, at least comparing players
# next, discards shuffle back into draw pile when draw_pile is out
# next, add bet functionality/money exchange
# next, add fold functionality
# next, add multiple rounds?

# print to console: cards you have (we can just do 1-52 for now), you input numbers 1-5, for the index of the cards you want to discard
# prints your new hand

# implementing scoring - score hands at end of round.
# check for pairs, 3 of a kind, 4 of a kind, straights, flushes
# representing the cards -- can do multiples. so 1-13 are the lowest ranked cards -- hearts i guess, and then 14-27 are the next, etc.
# so i could mod 14 to figure out the number and remainder 14 for the suit


# finished features: deal discard deal, multiple players, betting/folding, card representations
# todo: /organization/, scoring function, multiple rounds, discard shuffle back into draw pile,

import deck_class
import player_class


def deal_to_player(player, deck, num_cards):
    player.hand.extend(deck.deal(num_cards))
    print("Your hand:")
    player.print_hand()


def discard_and_draw(player, deck):
    print("Please enter the positions of the cards you'd like to discard, separated by spaces. Or press enter if you'd like not to discard anything.")
    # discard_input = str(input())
    d_input = input()
    if d_input.strip() == "":
        return
    hand_indeces = [int(card) for card in d_input.strip().split(" ")]
    discards = [player.hand[i-1] for i in hand_indeces]
    deck.discards.extend(discards)
    player.discard(discards)
    deal_to_player(player, deck, len(discards))


def play_game(num_players):
    deck = deck_class.Deck()
    players = []
    pot = 0
    ante = 2
    print("Welcome. You are playing a " + str(num_players) +
          "player game of poker where everyone starts with 20 chips. We'll start by ante-ing up.")

    #ante, shuffle
    for i in range(num_players):
        player = player_class.Player(id=i + 1)
        print("Player " + str(i + 1) +
              ". Please press enter to confirm your ante of " + str(ante) + " chips. Press 'D' to decline participation in this round.")
        if input() == 'd':
            player.active = False
        else:
            player.bet(ante)
            pot += ante
        players.append(player)
    deck.shuffle()

    #dealing, discarding, redealing
    for player in players:
        if not player.active:
            continue
        print("Player " + str(player.id) + ". Press enter to continue")
        input()
        deal_to_player(player, deck, 5)
        discard_and_draw(player, deck)
        if player.id == num_players:
            print("the round is over. press enter to continue to betting.")
        else:
            print("please pass to next player. press enter to continue.")
        input()

    # betting round
    active_players = [player for player in players if player.active]
    queue = active_players.copy()
    bet = ante
    while queue:
        player = queue.pop(0)
        print("Player " + str(player.id) + ". Press enter to continue")
        input()
        print("current bet = " + str(bet) + ". You've bet " +
              str(player.current_bet) + ". You have " + str(player.chips) + " chips remaining.")
        player.print_hand()
        print("Would you like to check/call(c), raise(r), or fold(f)?")
        p_input = input()
        if p_input == "c":
            print("You called the bet.")
            pot += player.bet(bet)
        elif p_input == "r":
            print("Please enter how much you'd like to raise the bet")
            new_bet = int(input())
            if new_bet < 1:
                print("Please enter a number higher than 0.")
                # input error cycles? more efficient way than this #TODO
                queue = [player] + queue
                continue
            print("You raised the bet by " + str(new_bet))
            bet += new_bet
            pot += player.bet(bet)
            queue.extend([p for p in active_players if p !=
                          player and p not in queue])
        elif p_input == "f":
            print("You folded.")
            active_players = [p for p in active_players if p != player]
            player.active = False
        else:
            print("bad input. please try again")
            queue = [player] + queue

    # round end; summary
    print("Round over. Active player hands: ")
    for player in active_players:
        print("Player " + str(player.id))
        player.print_hand()
    print("Inactive player hands:")
    for player in players:  # see if you can order by recency of fold
        if player in active_players:
            continue
        print("Player " + str(player.id))
        player.print_hand()


play_game(2)
