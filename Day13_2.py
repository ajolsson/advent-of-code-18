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
        
print("Advent of Code; day 13 task 2")

debug = False
debug_output = False

if debug == True:
    print("DEBUG")
    file_name = "Day13Data_test2.txt" #6,4
else:
    print("LIVE")
    file_name = "Day13Data.txt"

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
        # else:
        #     if char == " ":
        #         raise Exception("weird")
        matrix[x][y] = char

print(trains)

tracks = ""
for y in range(0, height):
    for x in range(0, width):
        tracks += matrix[x][y]
print(tracks)

print_tracks(matrix, trains)

def get_first_train(trains):
    smallest_y = None
    smallest_x = None
    first_train = None
    for train in trains:
        if smallest_y == None or train[4] < smallest_y:
            if smallest_x == None or train[3] < smallest_x:
                smallest_y = train[4]
                smallest_x = train[3]
                first_train = train
    return first_train

tick_count = 0
final_coord = None
while len(trains) > 1:
    tick_count += 1

    if tick_count % 1000 == 0:
        print(str(tick_count) + " ticks")

    for i in range(0, len(trains)): #find top left train
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
    
    new_trains = []
    for train in trains:
        train_x = train[3]
        train_y = train[4]
        does_collide = False
        for other_train in trains:
            if train[0] != other_train[0]:
                other_train_x = other_train[3]
                other_train_y = other_train[4]

                if train_x == other_train_x and train_y == other_train_y:
                    does_collide = True
                    print("Trains " + str(train[0]) + " and " + str(other_train[0]) + " collided (" + str(train[3]) + "," + str(train[4]) + "). " + str(len(trains) - 2) + " trains left.")
                    #print("Trains " + str(train[0]) + " and " + str(other_train[0]) + " collided.")
        if does_collide == False:
            new_trains.append(train)

    trains = new_trains
    
    if debug_output == True:
        print_tracks(matrix, trains)

final_coord = (trains[0][3], trains[0][4])

if final_coord != None:
    print_tracks(matrix, trains)
    print("Results: " + str(final_coord[0]) + "," + str(final_coord[1]))

#when trains crash, remove both
#when trains crash, continue exection
#when only one train left, get coordinates for the remaing train
#not 138,89

#rule of which train moves first!! It means, a cart that has moved can crash into another one??
#"Carts all move at the same speed; they take turns moving a single step at a time."