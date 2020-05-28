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
import bet


def _init_players(players, num_players):
    for i in range(num_players):
        player = player_class.Player(id=i + 1)
        players.append(player)


def ante_up(players, ante, pot):
    for player in players:
        print("Player " + player.id +
              ". Please press enter to confirm your ante of " + str(ante) + " chips. Press 'D' to decline participation in this round.")
        if input() == 'd':
            player.active = False
        else:
            player.bet(ante)
            pot += ante  # TODO make game_state.pot
    return pot


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


def deal(players, deck):
    active_players = [p for p in players if p.active]
    for player in active_players:
        print("Player " + str(player.id) + ". Press enter to continue")
        input()
        deal_to_player(player, deck, 5)
        discard_and_draw(player, deck)
        if player.id == len(players):
            print("the round is over. press enter to continue to betting.")
        else:
            print("please pass to next player. press enter to continue.")
        input()


def summary(players, pot):
    active_players = []
    inactive_players = []
    for player in players:
        if player.active:
            active_players.append(player)
        else:
            inactive_players.append(player)

    print("Round over. Active player hands: ")
    for player in active_players:
        print("Player " + str(player.id))
        player.print_hand()

    print("Inactive player hands:")
    for player in inactive_players:  # see if you can order by recency of fold
        print("Player " + str(player.id))
        player.print_hand()

    print("Pot: " + str(pot))


def play_game(num_players):
    deck = deck_class.Deck()
    players = []
    pot = 0
    ante = 2
    _init_players(players, num_players)
    print("Welcome. You are playing a " + str(num_players) +
          "player game of poker where everyone starts with 20 chips. We'll start by ante-ing up.")

    #ante, shuffle
    pot = ante_up(players, ante, pot)
    deck.shuffle()

    #dealing, discarding, redealing
    deal(players, deck)

    # betting round
    pot = bet.betting_round(players, ante, pot)

    # round end; summary
    summary(players, pot)


play_game(2)
