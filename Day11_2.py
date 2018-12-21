import time

print("Advent of Code; day 11 task 2")

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
    width = 6
    height = 6
    x = 89
else:
    print("LIVE")
    width = 300
    height = 300
    x = 0
    #serial_number = 18 #90,269,16
    #serial_number = 42 #232,251,12
    serial_number = 2568 #90,201,15

matrix = [[0 for x in range(width)] for y in range(height)] 

# print(get_power_level(8, 3, 5)) #4
# print(get_power_level(57, 122, 79)) #-5
# print(get_power_level(39, 217, 196)) #0
# print(get_power_level(71, 101, 153)) #4

i = 0
for xr in range(0, width):
    for yr in range(0, height):
        if debug == True:
            i += 1
            matrix[xr][yr] = i
        else:
            matrix[xr][yr] = get_power_level(serial_number, xr + 1, yr + 1)
        
max_sum = -1000000
max_coord = None
number_of_squares = 0

while x < width:

    start = time.time()
    if x % 10 == 0:
        print("X is: " + str(x))
    
    y = 0
    while y < height:

        max_width = width - x
        max_height = height - y
        max_sides = min(max_width, max_height)

        sides = 1

        previous_sum = 0
        while sides < max_sides + 1:
            number_of_squares += 1
            if number_of_squares % 100000 == 0:
                print("Number of squares: " + str(number_of_squares))
            x1 = x
            y1 = y
            sum = 0

            while y1 < y + sides:
                sum += matrix[x + sides - 1][y1]
                y1 += 1

            while x1 < x + sides - 1:
                sum += matrix[x1][y + sides - 1]
                x1 += 1
            
            sum += previous_sum

            if sum > max_sum:
                max_sum = sum
                max_coord = (x + 1, y + 1, sides, max_sum)
                print(max_sum, (x + 1, y + 1, sides))

            previous_sum = sum
            sides += 1
        
        y += 1
    
    end = time.time()
    x += 1

print("Result (" + str(max_coord[3]) + "): " + str(max_coord[0]) + "," + str(max_coord[1]) + "," + str(max_coord[2]))