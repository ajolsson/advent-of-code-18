print("Advent of Code; day 9 task 1")

debug = True
debug_output = True

if debug == True:
    print("DEBUG")
    
    # Example 1
    marbles = 25
    players = 9
else:
    print("LIVE")
    marbles = 493
    players = 71863

pos = -1

def next_value():
    global pos
    pos += 1
    return int(input[pos])


marbles_i = []
i = 0
while i < marbles:
    marbles[i] = i

pos = -1
def next_marble():
    global pos
    pos += 1
    return marbles_i[pos]