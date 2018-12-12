import re
import operator
from datetime import datetime

class ShiftLine:
    
    def __init__(self, shiftCode):
        match = re.search("^\[(.*)\] (.*)", shiftCode)
        self.dateTimeString = match.group(1)
        self.shiftLineTime = datetime.strptime(self.dateTimeString, "%Y-%m-%d %H:%M")
        self.text = match.group(2)

class GuardDay:
    
    def __init__(self, guardId):
        self.guardId = guardId
        self.minutesAsleep = {}

print("Advent of Code; day 4 task 1")
dataFile = open("day4Data.txt", "r")
#dataFile = open("day4Data_test1.txt", "r")

data = dataFile.readlines()
dataFile.close()

allShiftLines = []

for shiftLine in data:
    allShiftLines.append(ShiftLine(shiftLine))

currentGuardDay = None
asleep = None
guardDays = []

for shiftLine in sorted(allShiftLines, key = lambda x: x.shiftLineTime):
    if shiftLine.text[0] == "G":
        match = re.search("^.*(#\d*).*", shiftLine.text)
        currentGuardDay = GuardDay(match.group(1))
        guardDays.append(currentGuardDay)
        #print("gurrent guard id: " + currentGuardDay.guardId)

    elif shiftLine.text[0] == "f":
        asleep = shiftLine.shiftLineTime
        #print("sleep: " + str(asleep.minute))
    elif shiftLine.text[0] == "w":
        #print("wake: " + str(shiftLine.shiftLineTime.minute))
        minutes = shiftLine.shiftLineTime - asleep
        m = 0
        for minute in range(asleep.minute, shiftLine.shiftLineTime.minute):
            m += 1
            if minute in currentGuardDay.minutesAsleep:
                currentGuardDay.minutesAsleep[minute] += 1
            else:
                currentGuardDay.minutesAsleep[minute] = 1
        #print("minutes: " + str(m))
        #print(currentGuardDay.minutesAsleep)
    else:
        raise Exception("Case not handled: " + shiftLine.text)

#for guardDay in guardDays:
#    print(guardDay.guardId)
#    print(sum(guardDay.minutesAsleep.values()))

maxMinutes = -1
maxGuardDay = None
for guardDay in guardDays:
    if sum(guardDay.minutesAsleep.values()) > maxMinutes:
        maxMinutes = sum(guardDay.minutesAsleep.values())
        maxGuardDay = guardDay

combinedGuardDays = {}
currentGuardId = -1
for guardDay in guardDays:
    id = int(guardDay.guardId[1:])
    current = None
    if id in combinedGuardDays:
        current = combinedGuardDays[id]
    else:
        current = GuardDay(guardDay.guardId)
        combinedGuardDays[id] = current
    
    for m in range(0, 59):
        if m in guardDay.minutesAsleep:
            if m in current.minutesAsleep:
                current.minutesAsleep[m] += 1
            else:
                current.minutesAsleep[m] = 1

m = -1
highest = None
for guard in combinedGuardDays:
    guard_id = guard
    total_minutes_asleep = sum(combinedGuardDays[guard].minutesAsleep.values())
    if total_minutes_asleep > m:
        m = total_minutes_asleep
        highest = combinedGuardDays[guard]

print("GuardID: " + highest.guardId)
print("Minutes asleep: " + str(sum(highest.minutesAsleep.values())))
print("Max minute: " + str(max(highest.minutesAsleep, key=highest.minutesAsleep.get)))
print("Times asleep on this minute: " + str(highest.minutesAsleep[max(highest.minutesAsleep, key=highest.minutesAsleep.get)]))
print("Result: " + str(int(highest.guardId[1:]) * max(highest.minutesAsleep, key=highest.minutesAsleep.get)))