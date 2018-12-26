print("Advent of Code; day 16 task 2")

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
    def __init__(self, opcode, a, b, c):
        self.opcode = opcode
        self.a = a
        self.b = b
        self.c = c
        self.register_0_before = 0
        self.register_0_after = 0
        self.register_1_before = 0
        self.register_1_after = 0
        self.register_2_before = 0
        self.register_2_after = 0
        self.register_3_before = 0
        self.register_3_after = 0
    
    def parse(line1, line2, line3):
        opcode = int(line2.split()[0])
        a = int(line2.split()[1])
        b = int(line2.split()[2])
        c = int(line2.split()[3])

        i = Instruction(opcode, a, b, c)
        i.register_0_before = int(line1[9])
        i.register_0_after = int(line3[9])
        i.register_1_before = int(line1[12])
        i.register_1_after = int(line3[12])
        i.register_2_before = int(line1[15])
        i.register_2_after = int(line3[15])
        i.register_3_before = int(line1[18])
        i.register_3_after = int(line3[18])
        
        return i

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
codes = []
i = 0
while i < len(data):
    if data[i][0] == "B":
        line1 = data[i]
        line2 = data[i + 1]
        line3 = data[i + 2]

        instructions.append(Instruction.parse(line1, line2, line3))

        if len(line1) != 21:
            raise Exception(len(line1))

        if len(line3) != 21:
            raise Exception(len(line1))

        i += 3
    elif len(data[i]) > 2:
        result = data[i][:-1].split()
        codes.append(Instruction(int(result[0]), int(result[1]), int(result[2]), int(result[3])))
    i += 1

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

opcodes = {}

for i in instructions:
    for m in methods:
        device = Device(i.register_0_before, i.register_1_before, i.register_2_before, i.register_3_before)
        m(device, i)
        if device.check(i):
            if i.opcode not in opcodes:
                opcodes[i.opcode] = []

            if m not in opcodes[i.opcode]:
                opcodes[i.opcode].append(m)

opcode_methods = {}

while len(opcode_methods) < 16:
    for o in opcodes:
        if len(opcodes[o]) == 1:
            print("opcode: " + str(o) + ". Method: " + opcodes[o][0].__name__)
            opcode_methods[o] = opcodes[o][0]

            for op in opcodes:
                if opcode_methods[o] in opcodes[op]:
                    opcodes[op].remove(opcode_methods[o])

device = Device(0, 0, 0, 0)
for i in codes:
    m = opcode_methods[i.opcode]
    m(device, i)

print(device.registers[0])