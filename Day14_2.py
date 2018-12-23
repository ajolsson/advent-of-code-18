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
    count = -1
    sum = elves[0].current_recipe.score + elves[1].current_recipe.score
    elf_1 = elves[0].current_recipe.score + 1
    elf_2 = elves[1].current_recipe.score + 1
    for digit in str(sum):
        r = Recipe(int(digit))
        r.set_previous(last_recipe)
        r.set_next(first_recipe)
        recipes.append(r)
        last_recipe = r

        prev_recipe = last_recipe
        pattern = ""
        for _ in range(0, len(sequence)):
            pattern += str(prev_recipe.score)
            prev_recipe = prev_recipe.previous
        pattern = pattern[::-1]

        if pattern == sequence:
            count = len(recipes)

    for r in range(0, elf_1):
        elves[0].set_current_recipe(elves[0].current_recipe.next)

    for r in range(0, elf_2):
        elves[1].set_current_recipe(elves[1].current_recipe.next)

    return (last_recipe, count)

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

print("Advent of Code; day 14 task 2")

debug = False
debug_output = False

if debug:
    print("DEBUG")
    data = "37"
    #sequence = "91" #13
    #sequence = "51589" #9
    #sequence = "01245" #5
    #sequence = "92510" #18
    #sequence = "59414" #2018
    #sequence = "67792510" #15
    #sequence = "16" #14
    #sequence = "58916" #11
    sequence = "167792" #14

else:
    print("LIVE")
    data = "37"
    sequence = "157901" #20317612

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
count = -1
while count < 0:
    
    if i % 100000 == 0:
        print(i)
    i += 1

    last_recipe, count = combine_recipes(last_recipe)

    if debug_output:
        print_recipes()

print(count - len(sequence))