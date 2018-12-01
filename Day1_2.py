print("Advent of Code; day 1 task 2")
sequenceFile = open("sequenceFile.txt", "r")
#sequenceFile = open("testFile.txt", "r")
#sequenceFile = open("testFile2.txt", "r")

curSequence = 0
dicValues = {}
lineNumber = 0
iteration = 0
result = 0
hasResult = False

while (hasResult == False):
    iteration = iteration + 1

    lineNumber = 0
    sequenceFile.seek(0)
    for line in sequenceFile:
        lineNumber = lineNumber + 1
        lineValue = int(line)
        curSequence += lineValue
    
        if curSequence in dicValues:
            #print("repeated from " + str(dicValues[curSequence]) + ": " + str(curSequence)) #prints any 
            if hasResult == False:
                result = int(curSequence)
                hasResult = True

        dicValues[curSequence] = iteration

sequenceFile.close()
if hasResult == True:
    print("Result (in iteration " + str(iteration) + "): " + str(result))