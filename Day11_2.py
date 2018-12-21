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
    #serial_number = 18 #90,269,16
    serial_number = 42 #232,251,12
else:
    print("LIVE")
    serial_number = 2568 #90,201,15

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
number_of_squares = 0
x = 89
while x < width:

    start = time.time()
    if x % 10 == 0:
        print(x)
    
    y = 0
    while y < height:

        if y % 50 == 0:
            print(x, y)

        max_width = width - x - 1
        max_height = height - y - 1
        max_sides = min(max_width, max_height)

        sides = 1

        previous_sum = -1
        while sides < max_sides:
            number_of_squares += 1
            if number_of_squares % 100000 == 0:
                print("Number of squares: " + str(number_of_squares))
            x1 = x
            y1 = y
            sum = 0
            for x1 in range(x, x + sides):
            #for x1 in range(x + sides - 1, x + sides):
                for y1 in range(y, y + sides):
                #for y1 in range(y + sides - 1, y + sides):
                    sum += matrix[x1][y1]
            
#            sum += previous_sum

            if sum > max_sum:
                max_sum = sum
                max_coord = (x + 1, y + 1, sides, max_sum)
                print(max_sum, (x + 1, y + 1, sides))

            #previous_sum = sum
            sides += 1
        
        y += 1
    
    end = time.time()
    print(end - start)
    x += 1

#print(max_sum, max_coord)
print("Result (" + str(max_coord[3]) + "): " + str(max_coord[0]) + "," + str(max_coord[1]) + "," + str(max_coord[2]))