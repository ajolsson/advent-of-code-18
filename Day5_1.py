print("Advent of Code; day 5 task 1")
dataFile = open("day5Data.txt", "r")
#dataFile = open("day5Data_test2.txt", "r")

data = dataFile.read()
dataFile.close()

def remove_reactions(input, iterations):
    new_string = ""
    iterations += 1
    i = 0
    while i < len(input):
        if i < len(input) - 1 and input[i] != input[i + 1] and input[i].upper() == input[i + 1].upper():
            i += 2
        else:
            new_string += input[i]
            i += 1
    if (len(input) == len(new_string)):
        return new_string, iterations
    else:
        return remove_reactions(new_string, iterations)

output = remove_reactions(data, 0)
print("Result (" + str(output[1]) + " iterations): " + str(len(output[0])))