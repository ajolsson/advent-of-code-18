print("Advent of Code; day 7 task 2")

debug = True

if debug == True:
    print("DEBUG")
    dataFile = open("day7Data_test1.txt", "r") #15
    base_step_time = 1
    number_of_workers = 2
else:
    print("LIVE")
    dataFile = open("day7Data.txt", "r") #not 87
    base_step_time = 60
    number_of_workers = 6

data = dataFile.readlines()
dataFile.close()

def get_seconds(task):
    all_letters = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return base_step_time + all_letters.find(task)

def get_next_available_tasks_2(tasks, done_tasks, unavailable_tasks):
    no_dependencies = []
    for t in tasks:
        if t not in done_tasks:
            bust = False
            for s in steps:
                if t == s[1] and s[0] not in done_tasks:
                    bust = True
            if bust == False:
                if t not in unavailable_tasks:
                    no_dependencies.append(t)
    
    sorted_tasks = sorted(no_dependencies)
    return sorted_tasks

def get_next_available_task(tasks, done_tasks, unavailable_tasks):
    sorted_tasks = get_next_available_tasks_2(tasks, done_tasks, unavailable_tasks)

    if len(sorted_tasks) > 0:
        return min(sorted_tasks)
    else:
        return None

steps = []
for string in data:
    prereq = string[5]
    dependent = string[36]
    steps.append((prereq, dependent))

tasks = []
for s in steps:
    if s[0] not in tasks:
        tasks.append(s[0])
    if s[1] not in tasks:
        tasks.append(s[1])

#iterate over workers?
#iterate over seconds?

# Find the letters with no dependencies and put the first one (alpabetically) in the result
# Iterate, and check that that the previous letter is not checked for
done_tasks = []
unavailable_tasks = []
tasks_with_time = {}
#result_with_time = {}
workers_task = {}

for l in tasks:
    tasks_with_time[l] = get_seconds(l)

elapsed_seconds = 0

while len(done_tasks) < len(tasks):
    for i in range(0, number_of_workers):
        if i not in workers_task:
            task = get_next_available_task(tasks, done_tasks, unavailable_tasks)
            if task != None:
                tasks_with_time[task] = elapsed_seconds + get_seconds(task)
                workers_task[i] = task
                unavailable_tasks.append(task)
        else:
            task = workers_task[i]
            if tasks_with_time[task] < elapsed_seconds: #ready for new task
                done_tasks.append(task)

                task = get_next_available_task(tasks, done_tasks, unavailable_tasks)
                if task != None:
                    tasks_with_time[task] = elapsed_seconds + get_seconds(task)
                    workers_task[i] = task
                    unavailable_tasks.append(task)

    elapsed_seconds += 1


print(elapsed_seconds) #NOT 87

# while len(unavailable_letters) < len(letters):
#     available_tasks = get_next_available_task(letters, unavailable_letters)
#     if number_of_workers >= available_tasks:
#         for d in available_tasks:
#             elapsed_seconds += get_seconds(d)

    # assign a value of each task (seconds)
    # loop over each second
    # loop over each worker
    # if worker is free (task is done), assign next available task
    
    #find which tasks is done fastest, add the time, then get new tasks and repeat
    
    


    # for d in sorted_dependencies:
    #     elapsed_seconds += get_seconds(d)

    # m = min(available_tasks)
    # result.append(m)

# result_string = ''.join(result)
# print(result_string)

# print(get_seconds("A"))
# print(get_seconds("Z"))