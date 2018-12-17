print("Advent of Code; day 9 task 1")

debug = True
live = True
debug_output = False

if debug == True:
    print("DEBUG")

if live == True:
    print("LIVE")

def get_next_marble(marbles):
    if len(marbles) > 0:
        #return sorted(marbles)[0]
        return marbles[0]
    else:
        return -1

def play_game(number_of_players, number_of_marbles):

    marbles = []
    game = []
    player_marbles = []
    players = {}
    current_pos = 0

    i = 0
    while i <= number_of_marbles:
        marbles.append(i)
        i += 1

    i = 0
    while i < number_of_players:
        players[i] = []
        i += 1

    game.append(0)
    marbles.remove(0)

    do_continue = True
    while do_continue == True:
        for player in players:
            marble = get_next_marble(marbles) #take marble

            if debug_output == True and marble % 1000 == 0:
                print(marble)
            
            if marble == -1: #break if no marbles
                do_continue = False
                break

            if marble % 23 == 0: # every 23rd marble gives points
                players[player].append(marble)
                player_marbles.append(game[current_pos])
                
                # go 7 positions counter-clockwise
                if current_pos > 8:
                    current_pos -= 7
                else:
                    current_pos = len(game) - 7 + current_pos

                # add marble to player's score and remove from the game    
                players[player].append(game[current_pos])
                game.remove(game[current_pos])
                player_marbles.append(game[current_pos])

            else:
                if current_pos == len(game) - 1:
                    current_pos = 1    
                else:
                    current_pos += 2

                game.insert(current_pos, marble)
            
            # remove the marble
            marbles.remove(marble)

    max_sum = 0
    for player in players:
        value = sum(players[player])
        if (value > max_sum):
            max_sum = value

    if debug_output:
        print(len(game))
        print(len(marbles))
        print(len(player_marbles))
        print(len(game) + len(marbles) + len(player_marbles))
    return max_sum

def play_and_print(number_of_players, number_of_marbles, correct_result):
    result = play_game(number_of_players, number_of_marbles)
    print(str(result) + " (" + str(correct_result) + ": " + str(correct_result - result) + ")")

if debug == True:
    play_and_print(9, 25, 32)
    play_and_print(10, 1618, 8317)
    play_and_print(13, 7999, 146373)
    play_and_print(17, 1104, 2764)
    play_and_print(21, 6111, 54718)
    play_and_print(30, 5807, 37305)

if live == True:
    play_and_print(493, 71863, 367802)