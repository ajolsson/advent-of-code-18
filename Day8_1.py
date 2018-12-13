print("Advent of Code; day 8 task 1")

class Node:
    #number_of_child_nodes = -1
    #number_of_metadata = -1
    #node_data = -1

    def __init__(self, parent, node_data, number):
        self.parent = parent
        self.node_data = node_data
        self.number_of_child_nodes = int(node_data[0])
        self.number_of_metadata = int(node_data[1])
        self.meta_datas = []
        self.name = "Node " + str(number)
        self.child_data = self.node_data[2:len(self.node_data) - self.number_of_metadata]

    def print(self):
        print(self.name + " with " + str(self.number_of_child_nodes) + " child nodes.")

    def calculate_metadata(self):
        return sum(self.meta_datas)

debug = True
debug_output = True

if debug == True:
    print("DEBUG")
    dataFile = open("Day8Data_test1.txt", "r") #138
else:
    print("LIVE")
    dataFile = open("Day8Data.txt", "r") #

data = dataFile.read()
dataFile.close()

input = data.split()
print(input)

# def get_child_nodes(parent, input, number):
#     number += 1

#     pos = 0
#     for i in range(0, parent.number_of_child_nodes):
#         child = Node(parent, input, number) # get where the child end 
#         get_child_nodes(child, child.child_data, number)
        

#     #parent.child_nodes = get_child_nodes(parent, parent.child_data, number)
#     for c in parent.child_nodes:
#         return get_child_nodes(c, c.number_of_child_nodes, number)
    
    #number += 1
    #n = Node(parent, input, number)
    #n.print()

    #get_child_nodes

    # if len(input) > 0:
    #     return get_child_nodes(n, input[2:len(input) - n.number_of_metadata], number)
    # else:
    #     return n

    # if n.number_of_child_nodes > 0:
    #     return get_child_nodes(n, input[2:len(input) - n.number_of_metadata], number)
    #     #n.meta_datas = input[:len(input) - n.number_of_metadata] #always last, put in node
    # else:
    #     return n

#i = 0
# while i < len(input):
root = Node(None, input, i)
#root.print()
#r = get_child_nodes(root, input[2:len(input) - root.number_of_metadata], i)
#r = get_child_nodes(root, input[2:len(input) - root.number_of_metadata], i)
#print(r)


i = 0
while i < len(input):
    number_of_children = input[i]
    number_of_metadata = input[i+1]

    for c in range(number_of_children):
        
