print("Advent of Code; day 16 task 1")

class Device:
    def __init__(self, value1, value2, value3, value4):
        self.registers = []
        self.registers.append(value1)
        self.registers.append(value2)
        self.registers.append(value3)
        self.registers.append(value4)

    def check(self, instruction):
        return self.registers[0] == instruction.register_0_after and \
            self.registers[1] == instruction.register_1_after and \
            self.registers[2] == instruction.register_2_after and \
            self.registers[3] == instruction.register_3_after

class Instruction:
    def __init__(self, line1, line2, line3):
        self.opcode = int(line2.split()[0])
        self.a = int(line2.split()[1])
        self.b = int(line2.split()[2])
        self.c = int(line2.split()[3])
        self.register_0_before = int(line1[9])
        self.register_0_after = int(line3[9])
        self.register_1_before = int(line1[12])
        self.register_1_after = int(line3[12])
        self.register_2_before = int(line1[15])
        self.register_2_after = int(line3[15])
        self.register_3_before = int(line1[18])
        self.register_3_after = int(line3[18])

    def print(self):
        print("Before: [" + str(self.register_0_before) + ", " + str(self.register_1_before) + ", " + str(self.register_2_before) + ", " + str(self.register_3_before) + "]")
        print(str(self.opcode) + " " + str(self.a) + " " + str(self.b) + " " + str(self.c))
        print("After: [" + str(self.register_0_after) + ", " + str(self.register_1_after) + ", " + str(self.register_2_after) + ", " + str(self.register_3_after) + "]")

# addition
def addr(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] + device.registers[instruction.b]

def addi(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] + instruction.b

# multiplication
def mulr(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] * device.registers[instruction.b]

def muli(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] * instruction.b

#Bitwise AND
def banr(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] & device.registers[instruction.b]

def bani(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] & instruction.b

#Bitwise OR
def borr(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] | device.registers[instruction.b]

def bori(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a] | instruction.b

#assignment
def setr(device, instruction):
    device.registers[instruction.c] = device.registers[instruction.a]

def seti(device, instruction):
    device.registers[instruction.c] = instruction.a

#greater-than testing
def gtir(device, instruction):
    device.registers[instruction.c] = 1 if instruction.a > device.registers[instruction.b] else 0

def gtri(device, instruction):
    device.registers[instruction.c] = 1 if device.registers[instruction.a] > instruction.b else 0

def gtrr(device, instruction):
    device.registers[instruction.c] = 1 if device.registers[instruction.a] > device.registers[instruction.b] else 0

#equality testing
def eqir(device, instruction):
    device.registers[instruction.c] = 1 if instruction.a == device.registers[instruction.b] else 0

def eqri(device, instruction):
    device.registers[instruction.c] = 1 if device.registers[instruction.a] == instruction.b else 0

def eqrr(device, instruction):
    device.registers[instruction.c] = 1 if device.registers[instruction.a] == device.registers[instruction.b] else 0

debug_output = True

data_file = open("Day16Data.txt", "r")
data = data_file.readlines()
data_file.close()

instructions = []
i = 0
while i < len(data):
    if data[i][0] == "B":
        line1 = data[i]
        line2 = data[i + 1]
        line3 = data[i + 2]

        instructions.append(Instruction(line1, line2, line3))

        if len(line1) != 21:
            raise Exception(len(line1))

        if len(line3) != 21:
            raise Exception(len(line1))

        i += 4
    else:
        break

methods = []
methods.append(addr)
methods.append(addi)
methods.append(mulr)
methods.append(muli)
methods.append(banr)
methods.append(bani)
methods.append(borr)
methods.append(bori)
methods.append(setr)
methods.append(seti)
methods.append(gtir)
methods.append(gtri)
methods.append(gtrr)
methods.append(eqir)
methods.append(eqri)
methods.append(eqrr)

print(len(instructions))

instruction_result = []

for i in instructions:
    count = 0
    for m in methods:
        device = Device(i.register_0_before, i.register_1_before, i.register_2_before, i.register_3_before)
        m(device, i)
        if device.check(i):
            count += 1
    if count >= 3:
        instruction_result.append(i)

print(len(instruction_result))