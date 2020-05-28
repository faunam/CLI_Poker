
def betting_round(players, standing_bet, pot):
    active_players = [player for player in players if player.active]
    queue = active_players.copy()
    while queue:
        player = queue.pop(0)
        print("Player " + str(player.id) + ". Press enter to continue")
        input()
        print("standing bet = " + str(standing_bet) + ". You've bet " +
              str(player.current_bet) + ". You have " + str(player.chips) + " chips remaining.")
        player.print_hand()
        print("Would you like to check/call(c), raise(r), or fold(f)?")
        p_input = input()
        if p_input == "c":
            print("You called the bet.")
            pot += player.bet(standing_bet)
        elif p_input == "r":
            print("Please enter how much you'd like to raise the bet")
            p_raise = int(input())
            if p_raise < 1:
                print("Please enter a number higher than 0.")
                # input error cycles? more efficient way than this #TODO
                queue = [player] + queue
                continue
            print("You raised the bet by " + str(p_raise))
            standing_bet += p_raise
            pot += player.bet(standing_bet)
            queue.extend([p for p in active_players if p !=
                          player and p not in queue])
        elif p_input == "f":
            print("You folded.")
            active_players = [p for p in active_players if p != player]
            player.active = False
        else:
            print("bad input. please try again")
            queue = [player] + queue
    return pot
