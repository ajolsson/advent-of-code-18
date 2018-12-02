print("Advent of Code; day 2 task 1")
dataFile = open("day2Data.txt", "r")
#dataFile = open("day2Data_test1.txt", "r")

twice = 0
threeTimes = 0
checkSum = 0

for line in dataFile:
    charCount = {}
    locTwice = 0
    locThreeTimes = 0

    for char in line:
        if char in charCount:
            charCount[char] += 1
        else:
            charCount[char] = 1
    
    for key in charCount:
        if charCount[key] == 2:
            if locTwice == 0:
                locTwice += 1
        elif charCount[key] == 3:
            if locThreeTimes == 0:
                locThreeTimes += 1

    twice += locTwice
    threeTimes += locThreeTimes

dataFile.close()
print(twice * threeTimes)