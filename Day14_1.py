import time

class Elf:
    def __init__(self, number):
        self.number = number
        self.current_recipe = None
    
    def set_current_recipe(self, recipe):
        self.current_recipe = recipe

class Recipe:
    def __init__(self, number):
         self.score = number
         self.previous = self
         self.next = self
    
    def set_previous(self, recipe):
        self.previous = recipe
        recipe.next = self

    def set_next(self, recipe):
        self.next = recipe
        recipe.previous = self

def combine_recipes(last_recipe):
    sum = elves[0].current_recipe.score + elves[1].current_recipe.score
    elf_1 = elves[0].current_recipe.score + 1
    elf_2 = elves[1].current_recipe.score + 1
    for digit in str(sum):
        r = Recipe(int(digit))
        r.set_previous(last_recipe)
        r.set_next(first_recipe)
        recipes.append(r)

        last_recipe = r
    
    for r in range(0, elf_1):
        elves[0].set_current_recipe(elves[0].current_recipe.next)

    for r in range(0, elf_2):
        elves[1].set_current_recipe(elves[1].current_recipe.next)

    return last_recipe

def print_recipes():
    recipe = first_recipe
    if elves[0].current_recipe == recipe:
        result = "(" + str(recipe.score) + ")"
    elif elves[1].current_recipe == recipe:
        result = "[" + str(recipe.score) + "]"
    else:
        result = str(recipe.score)
    while recipe.next != first_recipe:
        recipe = recipe.next
        if elves[0].current_recipe == recipe:
            result += "(" + str(recipe.score) + ")"
        elif elves[1].current_recipe == recipe:
            result += "[" + str(recipe.score) + "]"
        else:
            result += str(recipe.score)

    print(result)

def count_recipes():
    count = 1
    recipe = first_recipe
    while recipe.next != first_recipe:
        recipe = recipe.next
        count += 1
    return count

print("Advent of Code; day 14 task 1")

debug = False
debug_output = False

if debug:
    print("DEBUG")
    data = "37"
    length = 10
    number_of_recipes = 9 #5158916779
    #number_of_recipes = 5 #0124515891
    #number_of_recipes = 18 #9251071085
    #number_of_recipes = 2018 #5941429882

else:
    print("LIVE")
    data = "37"
    length = 10
    number_of_recipes = 157901 #9411137133

recipes = []
first_recipe = None
prev_recipe = None
last_recipe = None
for digit in data:
    r = Recipe(int(digit))

    if prev_recipe != None:
        r.set_previous(prev_recipe)
    else:
        first_recipe = r

    recipes.append(r)
    prev_recipe = r
    last_recipe = r

last_recipe.set_next(first_recipe)

elves = []
elves.append(Elf(0))
elves.append(Elf(1))

elves[0].set_current_recipe(recipes[0])
elves[1].set_current_recipe(recipes[1])

if debug_output:
    print_recipes()

i = 0
#while count_recipes() < number_of_recipes + length:
while len(recipes) < number_of_recipes + length:
    
    if i % 5000 == 0:
        print(i)
    i += 1

    last_recipe = combine_recipes(last_recipe)
    
    if debug_output:
        print_recipes()

result = ""
next_recipe = first_recipe
for i in range(0, number_of_recipes + length):
    if i >= number_of_recipes:
        result += str(next_recipe.score)
    next_recipe = next_recipe.next

print(result)