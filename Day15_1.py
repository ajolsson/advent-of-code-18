import sys

class Game:
    def __init__(self, file_name, debug_output):
        self.board = Board(file_name)
        self.debug_output = debug_output
        self.active = True

    def run(self):
        print("run!")

        if debug_output:
            self.board.print(False)
            self.board.print(True)

        while self.active:
            units = self.board.get_live_units()
            any_unit_action = False
            for unit in units:
                if self.board.next_turn(unit):
                    any_unit_action = True
            
            if any_unit_action:
                self.board.turns += 1

            print("After turn: " + str(self.board.turns))
            self.board.print(True)
            input("Press Enter to continue...")

            if not any_unit_action:
                self.active = False
                print("Game ends")

                sum_health = 0
                live_units = self.board.get_live_units()
                for unit in live_units:
                    sum_health += unit.health
                print("Health: " + str(sum_health) + " (" + str(len(units)) + ") units.")
                print("Result: " + str(sum_health * self.board.turns))

class Unit:
    def __init__(self, type, x, y):
        self.type = type
        self.health = 200
        self.attack_power = 3
        self.node = None

    def attack(self, target):
        target.health -= self.attack_power

    def is_alive(self):
        return self.health > 0

class Board:
    def __init__(self, file_name):
        data_file = open(file_name, "r")
        self.data = data_file.readlines()
        data_file.close()
        self.width = len(self.data[0]) - 1
        self.height = len(self.data)
        self.matrix = [[0 for x in range(self.height)] for y in range(self.width)]
        self.nodes = [[None for x in range(self.height)] for y in range(self.width)]
        self.units = [] 
        self.turns = 0

        for x in range(0, self.width):
            for y in range(0, self.height):
                char = self.data[y][x]
                unit = None
                if char == "E" or char == "G":
                    unit = Unit(char, x, y)
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
            enemy = min(enemy_units, key = lambda e: (e.health, e.node.x, e.node.y)) #does it choose lowest in reading order?
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
                    enemy = min(enemy_units, key = lambda e: (e.health, e.node.x, e.node.y)) #does it choose lowest in reading order?
                    unit.attack(enemy)

        return completed_action

    def dijsktra(self, initial, end):

        if initial.x == 7 and initial.y == 4:
            print("this one should move up instead of left, as its y is lower")

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
        return self.is_open and (self.unit == None or not self.unit.is_alive)
    
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

print("Advent of Code; day 15 task 1")

debug_output = True

game = Game("Day15Data_test1.txt", True) #27730 (47*590)
game.run()

# game = Game("Day15Data_test2.txt", True)
# game.run()

# game = Game("Day15Data_test3.txt", True)
# game.run()

# game = Game("Day15Data.txt", True)
# game.run()

