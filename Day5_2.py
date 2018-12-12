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
    if (len(input) == len(new_string)):
        return new_string, iterations
    else:
        return remove_reactions(new_string, letter, iterations)

letters = {}
for c in data:
    if c.upper() not in letters:
        letters[c.upper()] = None

for k in letters:
    letters[k] = remove_reactions(data, k, 0)[0]
    print("Letter: " + k + ". Shorest polymer: " + str(len(letters[k])))
shortest = min(letters, key = lambda key: len(letters[key]))
print("Shortest: " + shortest + ". Result: " + str(len(letters[shortest])))