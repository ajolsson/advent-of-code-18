print("Advent of Code; day 8 task 1")

debug = False
debug_output = False

if debug == True:
    print("DEBUG")
    dataFile = open("Day8Data_test1.txt", "r") #66
else:
    print("LIVE")
    dataFile = open("Day8Data.txt", "r") #

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

def sum_metadata(children, metadata):
    result = sum(metadata)
    for c in children:
        result += sum_metadata(c[0], c[1])
    return result

def get_result(v):
    global value
    value += v
    return value

def get_nodevalue(children, metadata, result):
    if len(children) > 0:
        for m in metadata:
            if len(children) >= m:
                child = children[m - 1]
                get_nodevalue(child[0], child[1], result)
            else:
                result += 0
    else:
        get_result(sum(metadata))

    return get_result(0)

root = get_child_nodes()
value = 0
print(get_nodevalue(root[0], root[1], 0))