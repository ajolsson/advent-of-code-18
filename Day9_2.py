import time

print("Advent of Code; day 9 task 2")

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def set_left(self, node):
        self.left = node
        node.right = self

    def set_right(self, node):
        self.right = node
        node.left = self

debug = True
live = True
debug_output = True

if debug == True:
    print("DEBUG")

if live == True:
    print("LIVE")

def play_game(number_of_players, number_of_marbles):
    players = {}
    current_node = Node(0)
    current_node.set_left(current_node)
    current_node.set_right(current_node)

    i = 0
    while i < number_of_players:
        players[i] = []
        i += 1

    for marble in range(1, number_of_marbles + 1):
        if debug_output == True and marble % 500000 == 0:
            print(marble)

        if marble % 23 == 0: # every 23rd marble gives points
            players[marble % number_of_players].append(marble)
            
            # go 7 positions counter-clockwise
            for i in range(7):
                current_node = current_node.left

            # add marble to player's score and remove from the game    
            players[marble % number_of_players].append(current_node.value)

            current_node.left.set_right(current_node.right)
            current_node = current_node.right

        else:
            left_node = current_node.right
            right_node = left_node.right
            current_node = Node(marble)
            current_node.set_left(left_node)
            current_node.set_right(right_node)

    max_sum = 0
    for player in players:
        value = sum(players[player])
        if (value > max_sum):
            max_sum = value

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
    play_and_print(493, 71863, 367802)

if live == True:
    start = time.time()
    play_and_print(493, 71863100, 2996043280)
    end = time.time()
    print(end - start)