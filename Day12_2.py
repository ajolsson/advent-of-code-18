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

def get_results():
    result = 0
    for p in pots:
        if p.has_plant == True:
            result += p.number
    return result

def print_results(generation):
    print(str(generation) + ": " + str(get_results()))
        
print("Advent of Code; day 12 task 2")

debug = False
number_of_generations = 300
total_generations = 50000000000
initial_pots = 300

if debug == True:
    print("DEBUG")
    initial_state = "#..#.#..##......###...###"
    file_name = "Day12Data_test1.txt" #325
else:
    print("LIVE")
    initial_state = "##..#..##....#..#..#..##.#.###.######..#..###.#.#..##.###.#.##..###..#.#..#.##.##..###.#.#...#.##.."
    file_name = "Day12Data.txt" #4300000002414 (change: 86)

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
for pos in range(0, initial_pots):
    prev_left_pot = prev_left_pot.add_left()
    prev_right_pot = prev_right_pot.add_right()
    pots.append(prev_left_pot)
    pots.append(prev_right_pot)

previous_result = 0
for g in range(0, number_of_generations):
    previous_result = get_results()
    
    for p in pots:
        will_have_plant = next_generation(p)
        p.next_gen_plant = will_have_plant

    for p in pots:
        p.apply_next_gen()

results = get_results()
generation_change = results - previous_result

generations_to_calculate = total_generations - number_of_generations
forecast = generations_to_calculate * generation_change
forecast += results
print("Results: " + str(forecast))