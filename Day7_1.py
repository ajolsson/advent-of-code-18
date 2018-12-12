import re

print("Advent of Code; day 7 task 1")
dataFile = open("day7Data.txt", "r") #CQSWKZFJONPBEUMXADLYIGVRHT
#dataFile = open("day7Data_test1.txt", "r") #CABDFE

data = dataFile.readlines()
dataFile.close()

steps = []
for string in data:
    prereq = string[5]
    dependent = string[36]
    steps.append((prereq, dependent))

letters = []
for s in steps:
    if s[0] not in letters:
        letters.append(s[0])
    if s[1] not in letters:
        letters.append(s[1])
    
# Find the letters with no dependencies and put the first one (alpabetically) in the result
# Iterate, and check that that the previous letter is not checked for
result = []
while len(result) < len(letters):
    no_dependencies = []
    for l in letters:
        if l not in result:
            bust = False
            for s in steps:
                if l == s[1] and s[0] not in result:
                    bust = True
            if bust == False:
                no_dependencies.append(l)
    
    m = min(no_dependencies)
    result.append(m)

result_string = ''.join(result)
print(result_string)