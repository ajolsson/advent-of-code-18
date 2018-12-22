import re
import numpy as np
import matplotlib.pyplot as plt

print("Advent of Code; day 11 task 1")

def get_power_level(serial_number, x, y):
    rack_id = x + 10
    power_level = rack_id * y
    power_level = power_level + serial_number
    power_level = power_level * rack_id
    hundred_integer = (power_level // 100) % 10
    return hundred_integer - 5

debug = False
debug_output = True

if debug == True:
    print("DEBUG")
    serial_number = 42
else:
    print("LIVE")
    serial_number = 2568 #21,68

width = 300
height = 300

matrix = [[0 for x in range(width + 1)] for y in range(height +1 )] 

# print(get_power_level(8, 3, 5)) #4
# print(get_power_level(57, 122, 79)) #-5
# print(get_power_level(39, 217, 196)) #0
# print(get_power_level(71, 101, 153)) #4

for x in range(1, width + 1):
    for y in range(1, height + 1):
        matrix[x - 1][y - 1] = get_power_level(serial_number, x, y)

max_sum = -1
max_coord = None
x = 0
while x < width - 2:

    if x % 10 == 0:
        print(x)

    y = 0
    while y < height - 2:

        sum = matrix[x][y] + matrix[x][y + 1] + matrix[x][y + 2] + matrix[x + 1][y] + matrix[x + 1][y + 1] + matrix[x + 1][y + 2] + matrix[x + 2][y] + matrix[x + 2][y + 1] + matrix[x + 2][y + 2] 
        if sum > max_sum:
            max_sum = sum
            max_coord = (x + 1, y + 1)
        y += 1
    x += 1

print("Result: " + str(max_coord[0]) + "," + str(max_coord[1]))