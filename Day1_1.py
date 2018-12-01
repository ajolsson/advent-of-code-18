print("Advent of Code; day 1 task 1")
sequenceFile = open("sequenceFile.txt", "r")

curSequence = 0

for line in sequenceFile:
    lineValue = float(line)
    curSequence += lineValue
    #print(curSequence)

sequenceFile.close()
print(int(curSequence))