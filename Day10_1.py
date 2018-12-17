import re
import numpy as np
import matplotlib.pyplot as plt

print("Advent of Code; day 10 task 1")

class Point:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = x
        self.y = y
        self.velocity_x = vel_x
        self.velocity_y = vel_y

    def add_second(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def remove_second(self):
        self.x -= self.velocity_x
        self.y -= self.velocity_y

debug = False
debug_output = True

if debug == True:
    print("DEBUG")
    dataFile = open("Day10Data_test1.txt", "r") #HI
else:
    print("LIVE")
    dataFile = open("Day10Data.txt", "r") #GJNKBZEE ??

data = dataFile.readlines()
dataFile.close()

points = []

for line in data:
    match = re.search("(\-?\d*),\s*(-?\d*).*?(-?\d*),\s*(-?\d*)", line)
    x = int(match.group(1))
    y = int(match.group(2))
    vel_x = int(match.group(3))
    vel_y = int(match.group(4))

    p = Point(x, y, vel_x, vel_y)
    points.append(p)


max_diff_x = -1
max_diff_y = -1
max_total_diff = -1
smallest_second = -1
do_loop = True
i = 0
while do_loop == True:
    i += 1

    max_x = -1
    min_x = -1
    max_y = -1
    min_y = -1

    for point in points:
        point.add_second()
        
        if point.x > max_x:
            max_x = point.x

        if point.x < min_x:
            min_x = point.x

        if point.y > max_y:
            max_y = point.y

        if point.y < min_y:
            min_y = point.y

    
    diff_x = max_x - min_x
    diff_y = max_y - min_y
    diff_total = diff_x +diff_y

    if max_total_diff == -1:
        max_total_diff = diff_total

    if diff_total <= max_total_diff:
        max_total_diff = diff_total
    else:
        for point in points:
            point.remove_second()
        do_loop = False
        print(i - 1)

#Visualization
max_x = -1
min_x = -1
max_y = -1
min_y = -1

# Find min points
for point in points:
    if point.x < min_x:
        min_x = point.x

    if point.y < min_y:
        min_y = point.y

# Offset to positive numbers
diff_x = 0 - min_x
diff_y = 0 - min_y

# Add offset for all points
for point in points:
    point.x += diff_x
    point.y += diff_y

# Find max values for matrix
for point in points:
    if point.x > max_x:
        max_x = point.x

    if point.x < min_x:
        min_x = point.x

    if point.y > max_y:
        max_y = point.y

    if point.y < min_y:
        min_y = point.y

# make board
board = np.zeros([max_x, max_y], dtype=int) # should only be difference between max/min x/y
system = {}

# add point to matix
for point in points:
    system[(point.x - 1, point.y - 1)] = "0"

plt.imshow(board.T, origin='lower')

for point in system:
     plt.annotate(xy=point, s=system[point], ha='center', va='center')

plt.xticks([])
plt.yticks([])
plt.gca().invert_yaxis()
plt.show()