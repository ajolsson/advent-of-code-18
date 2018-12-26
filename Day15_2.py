import sys

class Game:
    def __init__(self, file_name, elf_attack_power, debug_output, stepwise_approval, unit_test):
        self.board = Board(file_name, elf_attack_power, unit_test)
        self.debug_output = debug_output
        self.active = True
        self.stepwise_approval = stepwise_approval
        self.unit_test = unit_test
        self.elf_attack_power = elf_attack_power

    def run(self):
        if self.debug_output:
            self.board.print(False)
            self.board.print(True)

        while self.active:

            for unit in self.board.units:
                if unit.type == "E" and unit.health < 1:
                    return False

            units = self.board.get_live_units()
            all_units_action = True
            for unit in units:
                if unit.is_alive():
                    if not self.board.next_turn(unit):
                        all_units_action = False
            
            if all_units_action:
                self.board.turns += 1

                if not self.unit_test:
                    print(self.board.turns)

            if self.debug_output:
                print("After turn: " + str(self.board.turns))
                self.board.print(True)
            
            if self.stepwise_approval:
                input("Press Enter to continue...")

            if not all_units_action:
                self.active = False

                if self.debug_output:
                    print("Game ends")

                sum_health = 0
                live_units = self.board.get_live_units()
                for unit in live_units:
                    sum_health += unit.health
                result = sum_health * self.board.turns
                
                if self.debug_output:
                    print("Health: " + str(sum_health) + " (" + str(len(units)) + ") units.")
                    print("Result: " + str(result))

                return result

class Unit:
    def __init__(self, type, x, y, attack_power):
        self.type = type
        self.health = 200
        self.attack_power = attack_power
        self.node = None

    def attack(self, target):
        target.health -= self.attack_power

    def is_alive(self):
        return self.health > 0

class Board:
    def __init__(self, file_name, elf_attack_power, unit_test):
        data_file = open(file_name, "r")
        self.data = data_file.readlines()
        data_file.close()
        self.width = len(self.data[0]) - 1
        self.height = len(self.data)
        self.matrix = [[0 for x in range(self.height)] for y in range(self.width)]
        self.nodes = [[None for x in range(self.height)] for y in range(self.width)]
        self.units = [] 
        self.turns = 0
        self.unit_test = unit_test
        self.elf_attack_power = elf_attack_power

        for x in range(0, self.width):
            for y in range(0, self.height):
                char = self.data[y][x]
                unit = None
                if char == "E" or char == "G":
                    attack_power = 3
                    if char == "E":
                        attack_power = elf_attack_power
                    unit = Unit(char, x, y, attack_power)
                    char = "."
                
                self.matrix[x][y] = char
                node = Node(x, y, y * self.width + x)
                node.is_open = char == "."
                
                if unit != None:
                    node.set_unit(unit)
                    self.units.append(unit)

                self.nodes[x][y] = node

        for x in range(0, self.width):
            for y in range(0, self.height):
                node = self.nodes[x][y]

                if node.x - 1 > 0:
                    node.set_left(self.nodes[x - 1][y])
                if node.y - 1 > 0:
                    node.set_up(self.nodes[x][y - 1])
                if node.x + 1 < self.width:
                    node.set_right(self.nodes[x + 1][y])
                if node.y + 1 < self.height:
                    node.set_down(self.nodes[x][y + 1])

    def print(self, include_units):
        board = ""
        for y in range(0, self.height):
            extension = ""
            for x in range(0, self.width):
                node = self.nodes[x][y]
                to_print = ""
                if include_units and node.unit != None and node.unit.is_alive():
                    to_print += node.unit.type
                    if len(extension) > 0:
                        extension += ", "
                    else:
                        extension += "   "
                    extension += node.unit.type + "(" + str(node.unit.health) + ")" #G(200)
                else:
                    if node.is_open:
                        to_print = "."
                    else:
                        to_print = "#"
                board += to_print
            if include_units:
                board += extension
            board += "\n"
        print(board)
    
    def get_live_units(self):
        units = list(filter(lambda u: u.health > 0, self.units))
        units.sort(key = lambda l: (l.node.y, l.node.x))
        return units

    def move_unit(self, from_node, to_node):
        unit = from_node.unit
        from_node.unit = None
        to_node.unit = unit
        unit.node = to_node

    def next_turn(self, unit):

        # if (self.turns == 37 and not self.unit_test):
        #     print("debug point")

        completed_action = False

        enemy_units = self.get_enemy_units(unit)
        if len(enemy_units) == 0:
            return False

        target_nodes = [] #all open squares adjacent to enemies
        for enemy in enemy_units:
            nodes = enemy.node.get_available_moves()
            for node in nodes:
                if node not in target_nodes:
                    target_nodes.append(node)

        #attack
        enemy_units = self.get_adjacent_enemies(unit)
        if len(enemy_units) > 0:
            enemy = min(enemy_units, key = lambda e: (e.health, e.node.y, e.node.x))
            unit.attack(enemy)
            completed_action = True
        
        # move
        else:
            min_distance = None
            closest_option = None
            next_move = None
            for option in target_nodes:
                path = self.dijsktra(unit.node, option) #finds the target, but doesn't choose the path that has the first step in reading order
                if path == None:
                    continue
                distance = len(path)
                if min_distance == None or distance < min_distance:
                    min_distance = distance
                    closest_option = option
                    next_move = path[1]
                elif min_distance == distance:
                    if option.sort_order < closest_option.sort_order:
                        closest_option = option
                        next_move = path[1]

            if next_move != None:
                self.move_unit(unit.node, next_move)
                completed_action = True
            
                enemy_units = self.get_adjacent_enemies(unit)
                if len(enemy_units) > 0:
                    enemy = min(enemy_units, key = lambda e: (e.health, e.node.y, e.node.x))
                    unit.attack(enemy)

        #return completed_action
        return True

    def dijsktra(self, initial, end):

        if initial.x == 1000 and initial.y == 1000:
            print("debug option...")

        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        shortest_paths = {initial: (None, 0)}
        current_node = initial 
        visited = set()
        
        while current_node != end:
            visited.add(current_node)
            destinations = current_node.get_available_moves()
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = 1 + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight, next_node.sort_order)
                    #shortest_paths[next_node] = (current_node, weight) #if same weight, choose lowest y?
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        #shortest_paths[next_node] = (current_node, weight)
                        shortest_paths[next_node] = (current_node, weight, next_node.sort_order)
            
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return None
            # next node is the destination with the lowest weight
            #current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
            current_node = min(next_destinations, key = lambda k: (next_destinations[k][1], next_destinations[k][2]))
        
        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path

    def get_adjacent_enemies(self, unit):
        units = []

        if unit.node.left != None and unit.node.left.unit != None and unit.node.left.unit.type != unit.type:
            if unit.node.left.unit.is_alive():
                units.append(unit.node.left.unit)
        if unit.node.up != None and unit.node.up.unit != None and unit.node.up.unit.type != unit.type:
            if unit.node.up.unit.is_alive():
                units.append(unit.node.up.unit)
        if unit.node.right != None and unit.node.right.unit != None and unit.node.right.unit.type != unit.type:
            if unit.node.right.unit.is_alive():
                units.append(unit.node.right.unit)
        if unit.node.down != None and unit.node.down.unit != None and unit.node.down.unit.type != unit.type:
            if unit.node.down.unit.is_alive():
                units.append(unit.node.down.unit)

        return units

    def get_enemy_units(self, unit):
         return list(filter(lambda u: u.type != unit.type and u.health > 0, self.units))
    
class Node:
    def __init__(self, x, y, sort_order):
        self.x = x
        self.y = y
        self.left = None
        self.up = None
        self.right = None
        self.down = None
        self.unit = None
        self.is_open = False
        self.unit = None
        self.sort_order = sort_order
    
    def set_left(self, node):
        self.left = node

    def set_up(self, node):
        self.up = node

    def set_right(self, node):
        self.right = node

    def set_down(self, node):
        self.down = node

    def is_available(self):
        return self.is_open and (self.unit == None or not self.unit.is_alive())
    
    def set_unit(self, unit):
        self.unit = unit
        unit.node = self

    def get_available_moves(self):
        nodes = []
        if self.left != None and self.left.is_available():
            nodes.append(self.left)
        if self.up != None and self.up.is_available():
            nodes.append(self.up)
        if self.right != None and self.right.is_available():
            nodes.append(self.right)
        if self.down != None and self.down.is_available():
            nodes.append(self.down)
        return nodes

print("Advent of Code; day 15 task 2")

debug_output = True
stepwise_approval = True

def run_unit_tests():
    game = Game("Day15Data_test1.txt", 15, False, False, True) #4988 (29*172)
    sum = game.run()
    print(sum == 4988)

    game = Game("Day15Data_test5.txt", 4, False, False, True) #31284 (33*948)
    sum = game.run()
    print(sum == 31284)

    game = Game("Day15Data_test6.txt", 15, False, False, True) #3478 (37*94)
    sum = game.run()
    print(sum == 3478)

    game = Game("Day15Data_test7.txt", 12, False, False, True) #6474 (39*166)
    sum = game.run()
    print(sum == 6474)

    game = Game("Day15Data_test8.txt", 34, False, False, True) #1140 (30*38)
    sum = game.run()
    print(sum == 1140)

def get_results(file_name, debug_output, stepwise_approval, unit_test):
    elf_attack_power = 4
    while True:
        print("Trying with attack power: " + str(elf_attack_power) + "...")
        game = Game(file_name, elf_attack_power, debug_output, stepwise_approval, unit_test)
        r = game.run()
        if r != False:
            return str(r) + " (attack power: " + str(elf_attack_power) + ")"
        elf_attack_power += 1

run_unit_tests()
#print(get_results("Day15Data_test1.txt", False, False, False))
#print(get_results("Day15Data_test5.txt", False, False, False))
print(get_results("Day15Data.txt", False, False, False)) #52688 (23 attack power)
# game = Game("Day15Data.txt", debug_output, stepwise_approval, False) #213692 (82*2606)