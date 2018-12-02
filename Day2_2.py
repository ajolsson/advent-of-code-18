print("Advent of Code; day 2 task 2")
dataFile = open("day2Data.txt", "r")
#dataFile = open("day2Data_test2.txt", "r")

data = dataFile.readlines()
dataFile.close()

filePos = 0

for outerLine in data:
    filePos += 1
    for innerLine in data[filePos:]:
        pos = 0
        matches = ""
        for char in outerLine:
            if innerLine[pos] == char:
                matches += char
            pos += 1

        if len(outerLine) == len(matches) + 1:
            print("First match: " + outerLine)
            print("Second match: " + innerLine)
            print("Result: " + matches)