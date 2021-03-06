import time

class Pot:

    def __init__(self, number, has_plant):
        self.number = number
        self.has_plant = has_plant
        self.left = None
        self.right = None
        self.next_gen_plant = False

    def set_left(self, pot):
        self.left = pot
    
    def set_right(self, pot):
        self.right = pot

    def get_local_pattern(self):
        if self.has_plant:
            return "#"
        return "."

    def get_pattern(self):
        pattern = ""

        if self.left != None:
            if self.left.left != None:
                pattern += self.left.left.get_local_pattern()
            else:
                pattern += "."
            pattern += self.left.get_local_pattern()
        else:
            pattern += ".."

        pattern += self.get_local_pattern()

        if self.right != None:
            pattern += self.right.get_local_pattern()

            if self.right.right != None:
                pattern += self.right.right.get_local_pattern()
            else:
                pattern += "."
        else:
            pattern += ".."

        return pattern

    def apply_next_gen(self):
        self.has_plant = self.next_gen_plant

    def add_left(self):
        pot = Pot(self.number - 1, False)
        self.set_left(pot)
        pot.set_right(self)
        return pot

    def add_right(self):
        pot = Pot(self.number + 1, False)
        self.set_right(pot)
        pot.set_left(self)
        return pot
    
def next_generation(pot):
    pattern = pot.get_pattern()
    for k in keys:
        if pattern == k:
            return keys[k]
    return False
        
print("Advent of Code; day 12 task 1")

debug = False
debug_output = False

if debug == True:
    print("DEBUG")
    initial_state = "#..#.#..##......###...###"
    file_name = "Day12Data_test1.txt" #325
else:
    print("LIVE")
    initial_state = "##..#..##....#..#..#..##.#.###.######..#..###.#.#..##.###.#.##..###..#.#..#.##.##..###.#.#...#.##.."
    file_name = "Day12Data.txt" #3793

data_file = open(file_name, "r")
data = data_file.readlines()
data_file.close()

keys = {}
for line in data:
    will_have_plant = line[9] == "#"
    key = line[0:5]
    keys[key] = will_have_plant

pots = []

prev_pot = None
first_pot = None
last_pot = None
for pos in range(0, len(initial_state)):
    has_plant = initial_state[pos] == "#"
    pot = Pot(pos, has_plant)
    pot.set_left(prev_pot)

    if prev_pot != None:
        prev_pot.set_right(pot)

    if pos == 0:
        first_pot = pot

    pots.append(pot)
    prev_pot = pot

last_pot = pot

prev_left_pot = first_pot
prev_right_pot = last_pot
for pos in range(0, 20):
    prev_left_pot = prev_left_pot.add_left()
    prev_right_pot = prev_right_pot.add_right()
    pots.append(prev_left_pot)
    pots.append(prev_right_pot)

if debug_output == True:
    pattern = ""
    for p in pots:
        pattern += p.get_local_pattern()
    print(pattern)

for g in range(0, 20):
    for p in pots:
        will_have_plant = next_generation(p)
        p.next_gen_plant = will_have_plant

    for p in pots:
        p.apply_next_gen()


if debug_output == True:
    pattern = ""
    for p in pots:
        pattern += p.get_local_pattern()
    print(pattern)

if debug_output == True:
    for p in pots:
        print(p.number, p.get_local_pattern())

result = 0
for p in pots:
    if p.has_plant == True:
        result += p.number

print("Result: " + str(result))