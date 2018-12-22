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
                if trains[i][3] == x and trains[i][4] == y:
                    tracks += trains[i][1]
                    has_train = True
                i += 1
            
            if has_train == False:
                tracks += matrix[x][y]
    print(tracks)
        
print("Advent of Code; day 13 task 1")

debug = False

if debug == True:
    print("DEBUG")
    file_name = "Day13Data_test1.txt" #7,3
else:
    print("LIVE")
    file_name = "Day13Data.txt" #117,62

data_file = open(file_name, "r")
data = data_file.readlines()
data_file.close()

# crash_coord = (7, 3)

width = len(data[0])
height = len(data)

print(width, height)

matrix = [[0 for x in range(height)] for y in range(width)]
trains = []

train_count = 0
for x in range(0, width):
    for y in range(0, height):
        char = data[y][x]
        if char == ">" or char == "<":
            trains.append((train_count, char, "l", x, y))
            train_count += 1
            char = "-"
        elif char == "v" or char == "^":
            trains.append((train_count, char, "l", x, y))
            train_count += 1
            char = "|"
        matrix[x][y] = char

print(trains)

tracks = ""
for y in range(0, height):
    for x in range(0, width):
        tracks += matrix[x][y]
print(tracks)

print_tracks(matrix, trains)

collision = False
tick_count = 0
crash_coord = None
while collision == False:
    tick_count += 1
    next_trains = []
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

        trains[i] = (trains[i][0], new_direction, new_next_turn, next_x, next_y)
    
    train_positions = {}
    for train in trains:
        train_x = train[3]
        train_y = train[4]
        if train_x in train_positions:
            if train_y in train_positions[train_x]:
                collision = True
                crash_coord = (train_x, train_y)
        else:
            train_positions[train[3]] = []

        train_positions[train[3]].append(train[4])

    #print_tracks(matrix, trains)

if crash_coord != None:
    print(tick_count)
    print("Results: " + str(crash_coord[0]) + "," + str(crash_coord[1]))

# mind the intersections; when the train is on the intersection,
# the rules for the next coordinate will be difference