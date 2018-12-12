import re

print("Advent of Code; day 6 task 1")
dataFile = open("day6Data.txt", "r") #4233
#dataFile = open("day6Data_test1.txt", "r") #17

data = dataFile.readlines()
dataFile.close()

def calculate_distance(p1, p2, q1, q2):
    return abs(p1 - q1) + abs(p2 - q2)

def count_distances(distance, distances):
    count = 0
    for d in distances:
        if d[1] == distance:
            count += 1
    return count

coords = []
min_x = -1
max_x = -1
min_y = -1
max_y = -1

for coord in data:
    match = re.search("^(\d*), (\d*)", coord)
    local_x = int(match.group(1))
    local_y = int(match.group(2))
    coords.append((local_x, local_y))

    if max_x == -1 or local_x > max_x:
        max_x = local_x
    
    if min_x == -1 or local_x < min_x:
        min_x = local_x
    
    if max_y == -1 or local_y > max_y:
        max_y = local_y
    
    if min_y == -1 or local_y < min_y:
        min_y = local_y

print("width: " + str(max_x))
print("height: " + str(max_y))

matrix = [[["."] for x in range(max_y + 1)] for y in range(max_x + 1)]

for x in range(max_x + 1):
    if x % 10 == 0:
        print(x)
    
    for y in range(max_y + 1):
        distances = []
        
        for c in coords:
            distance = (c, calculate_distance(c[0], c[1], x, y))
            distances.append(distance)

        min_distance = min(distances, key = lambda x: x[1])
        count = count_distances(min_distance[1], distances)
        if count == 1: #choose only if unique
            matrix[x][y] = min_distance[0]

border_coords = {}
for x in range(max_x + 1):
    for y in range(max_y + 1):
        if matrix[x][y][0] != ".":
            if x == 0 or x == max_x or y == 0 or y == max_y:
                border_coords[matrix[x][y]] = 1

count = {}
double_count = 0
for x in range(max_x + 1):
    for y in range(max_y + 1):
        if matrix[x][y][0] != "." and matrix[x][y] not in border_coords:
            if matrix[x][y] in count:
                count[matrix[x][y]] += 1
            else:
                count[matrix[x][y]] = 1

print("real:")
print(count)

print("border coordinates:")
print(border_coords)

max_area = max(count, key = lambda x: count[x])
print("Result: " + str(count[max_area]))