import re

class Claim:
    
    def __init__(self, claimCode):
        match = re.search("^#(\d*) @ (\d*),(\d*): (\d*)x(\d*)", claimCode)
        self.id = match.group(1)
        self.left = int(match.group(2)) + 1
        self.top = int(match.group(3)) + 1
        self.width = int(match.group(4))
        self.height = int(match.group(5))

    def right(self):
        return self.left + self.width - 1

    def bottom(self):
        return self.top + self.height - 1

    def containsCoordinates(self, x, y):
        return self.left <= x and self.right() >= x and self.top <= y and self.bottom() >= y


print("Advent of Code; day 3 task 1")
dataFile = open("day3Data.txt", "r")
#dataFile = open("day3Data_test1.txt", "r")

data = dataFile.readlines()
dataFile.close()

totalWidth = -1
totalHeight = -1
allClaims = []

for claim in data:
    allClaims.append(Claim(claim))    

for claim in allClaims:
    if claim.right() > totalWidth:
        totalWidth = claim.right()
    
    if claim.bottom() > totalHeight:
        totalHeight = claim.bottom()

print("width: " + str(totalWidth))
print("height: " + str(totalHeight))

matrix = [[0 for x in range(totalWidth + 1)] for y in range(totalHeight + 1)] 

for claim in allClaims:
    for x in range(claim.left - 1, claim.left - 1 + claim.width):
        for y in range(claim.top - 1, claim.top - 1 + claim.height):
            matrix[x][y] += 1

totalCount = 0
for x in range(totalWidth):
    for y in range(totalHeight):
        if matrix[x][y] > 1:
            totalCount += 1

print("Total overlapped: " + str(totalCount))

for claim in allClaims:
    overlapped = False
    for x in range(claim.left - 1, claim.left - 1 + claim.width):
        for y in range(claim.top - 1, claim.top - 1 + claim.height):
            if matrix[x][y] > 1:
                overlapped = True
    if overlapped == False:
        print("Not overlapped ID: " + claim.id)