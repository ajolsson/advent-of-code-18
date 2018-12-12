print("Advent of Code; day 5 task 2")
dataFile = open("day5Data.txt", "r")
#dataFile = open("day5Data_test2.txt", "r")

data = dataFile.read()
dataFile.close()

def remove_reactions(input, letter, iterations):
    new_string = ""
    iterations += 1
    i = 0
    while i < len(input):
        if i < len(input) - 1 and input[i] != input[i + 1] and input[i].upper() == input[i + 1].upper():
            i += 2
        else:
            if input[i].upper() != letter:
                new_string += input[i]
            i += 1
    
    return new_string, iterations
    
letters = {}
for c in data:
    if c.upper() not in letters:
        letters[c.upper()] = None

for k in letters:
    length = len(data)
    new_string = data
    i = -1
    while i < 0:
        length = len(new_string)
        new_string = remove_reactions(new_string, k , 0)[0]
        if length == len(new_string):
            i = 1
            letters[k] = new_string
            print("Letter: " + k)

shortest = min(letters, key = lambda key: len(letters[key]))
print("Shortest: " + shortest + ". Result: " + str(len(letters[shortest])))