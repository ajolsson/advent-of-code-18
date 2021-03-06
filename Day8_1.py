print("Advent of Code; day 8 task 1")

debug = False
debug_output = False

if debug == True:
    print("DEBUG")
    dataFile = open("Day8Data_test1.txt", "r") #138
else:
    print("LIVE")
    dataFile = open("Day8Data.txt", "r") #46962

data = dataFile.read()
dataFile.close()

input =  data.split()
pos = -1

def next_value():
    global pos
    pos += 1
    return int(input[pos])

def get_child_nodes():
    number_of_child_nodes = next_value()
    number_of_metadata = next_value()

    if debug_output:
        print(pos, number_of_child_nodes, number_of_metadata)

    children = []
    metadata = []

    for _ in range(number_of_child_nodes):
        children.append(get_child_nodes())

    for _ in range(number_of_metadata):
        metadata.append(next_value())

    return (children, metadata)

def get_metadata(children, metadata):
    result = sum(metadata)
    for c in children:
        result += get_metadata(c[0], c[1])
    return result

root = get_child_nodes()
print(get_metadata(root[0], root[1]))