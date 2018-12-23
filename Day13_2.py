import time

def print_tracks(matrix, trains):
    width = len(matrix)
    height = len(matrix[0])
    tracks = ""
    for y in range(0, height):
        for x in range(0, width):
            has_train = False
            i = 0
            while i < len(trains) and has_train == False:
                if trains[i][3] == x and trains[i][4] == y and trains[i][5]:
                    tracks += trains[i][1]
                    has_train = True
                i += 1
            
            if has_train == False:
                tracks += matrix[x][y]
    print(tracks)

def get_trains_in_order(trains):
    trains = list(filter(lambda t: t[5], trains))
    trains.sort(key = lambda l: (l[4], l[3]))
    return trains
        
print("Advent of Code; day 13 task 2")

debug = False
debug_output = False

if debug:
    print("DEBUG")
    file_name = "Day13Data_test2.txt" #6,4
else:
    print("LIVE")
    file_name = "Day13Data.txt" #69,67

data_file = open(file_name, "r")
data = data_file.readlines()
data_file.close()

width = len(data[0])
height = len(data)

if debug_output:
    print(width, height)

matrix = [[0 for x in range(height)] for y in range(width)]
trains = []

train_count = 0
for x in range(0, width):
    for y in range(0, height):
        char = data[y][x]
        if char == ">" or char == "<":
            trains.append((train_count, char, "l", x, y, True))
            train_count += 1
            char = "-"
        elif char == "v" or char == "^":
            trains.append((train_count, char, "l", x, y, True))
            train_count += 1
            char = "|"

        matrix[x][y] = char

if debug_output:
    print(trains)

if debug_output:
    tracks = ""
    for y in range(0, height):
        for x in range(0, width):
            tracks += matrix[x][y]
    print(tracks)

if debug_output:
    print_tracks(matrix, trains)

tick_count = 0
final_coord = None

while len(list(filter(lambda t: t[5], trains))) > 1:
    tick_count += 1

    if debug_output and tick_count % 1000 == 0:
        print(str(tick_count) + " ticks")

    trains = get_trains_in_order(trains)
    for i in range(0, len(trains)):
        direction = trains[i][1]
        next_turn = trains[i][2]
        x = trains[i][3]
        y = trains[i][4]
        if direction == ">":
            next_x = x + 1
            next_y = y
        elif direction == "<":
            next_x = x - 1
            next_y = y
        elif direction == "^":
            next_x = x
            next_y = y - 1
        elif direction == "v":
            next_x = x
            next_y = y  + 1
        else:
            raise Exception("Unsupported direction")
        
        new_direction = direction
        new_next_turn = next_turn
        if matrix[next_x][next_y] == "/":
            if direction == "^":
                new_direction = ">"
            elif direction == "v":
                new_direction = "<"
            elif direction == "<":
                new_direction = "v"
            elif direction == ">":
                new_direction = "^"

        elif matrix[next_x][next_y] == "\\":
            if direction == "^":
                new_direction = "<"
            elif direction == "v":
                new_direction = ">"
            elif direction == "<":
                new_direction = "^"
            elif direction == ">":
                new_direction = "v"

        elif matrix[next_x][next_y] == "+":
            if next_turn == "l":
                if direction == "^":
                    new_direction = "<"
                elif direction == "v":
                    new_direction = ">"
                elif direction == "<":
                    new_direction = "v"
                elif direction == ">":
                    new_direction = "^"
                new_next_turn = "s"
            if next_turn == "s":
                new_direction = direction
                new_next_turn = "r"
            if next_turn == "r":
                if direction == "^":
                    new_direction = ">"
                elif direction == "v":
                    new_direction = "<"
                elif direction == "<":
                    new_direction = "^"
                elif direction == ">":
                    new_direction = "v"
                new_next_turn = "l"

        does_collide = False
        for j in range(0, len(trains)):
            other_train = trains[j]
            if trains[i][0] != other_train[0]:
                other_train_x = other_train[3]
                other_train_y = other_train[4]

                if next_x == other_train_x and next_y == other_train_y:
                    if trains[i][5] and other_train[5]:
                        does_collide = True
                        trains[i] = (trains[i][0], new_direction, new_next_turn, next_x, next_y, False)
                        trains[j] = (trains[j][0], trains[j][1], trains[j][2], trains[j][3], trains[j][4], False)
                        print("Collision at " + str(next_x) + "," + str(next_y) + " after " + str(tick_count) + " ticks.")
        
        if does_collide == False:
            trains[i] = (trains[i][0], new_direction, new_next_turn, next_x, next_y, trains[i][5])
    
    if debug_output:
        print_tracks(matrix, trains)

trains = get_trains_in_order(trains)
final_coord = (trains[0][3], trains[0][4])

if final_coord != None:
    
    if debug_output:
        print_tracks(matrix, trains)
    
    print("Result: " + str(final_coord[0]) + "," + str(final_coord[1]))