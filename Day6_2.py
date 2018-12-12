import re

print("Advent of Code; day 6 task 2")
dataFile = open("day6Data.txt", "r") #45290
#dataFile = open("day6Data_test1.txt", "r") #17

data = dataFile.readlines()
dataFile.close()

def calculate_distance(p1, p2, q1, q2):
    return abs(p1 - q1) + abs(p2 - q2)

def sum_distances(distance):
    total_distance = 0
    for d in distances:
        total_distance += d[1]
    return total_distance

coords = []
min_x = -1
max_x = -1
min_y = -1
max_y = -1
min_distance_sum = 10000

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

count = 0
for x in range(max_x + 1):
    if x % 10 == 0:
        print(x)
    
    for y in range(max_y + 1):
        distances = []
        
        for c in coords:
            distance = (c, calculate_distance(c[0], c[1], x, y))
            distances.append(distance)

        distance_sum = sum_distances(distances)

        if distance_sum < min_distance_sum:
            count += 1

print("Result: " + str(count))