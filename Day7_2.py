print("Advent of Code; day 7 task 2")

debug = False
debug_output = True

if debug == True:
    print("DEBUG")
    dataFile = open("day7Data_test1.txt", "r") #15
    number_of_workers = 2
else:
    print("LIVE")
    dataFile = open("day7Data.txt", "r") #914
    number_of_workers = 5

data = dataFile.readlines()
dataFile.close()
all_letters = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_seconds(task):
    base_step_time = 60 + all_letters.find(task)
    if debug:
        return base_step_time - 60
    else:
        return base_step_time

def get_next_available_tasks(tasks, done_tasks, unavailable_tasks):
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
    sorted_tasks = get_next_available_tasks(tasks, done_tasks, unavailable_tasks)

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

done_tasks = []
unavailable_tasks = []
workers_task = {}
tasks_with_time = {}
elapsed_seconds = 0

while len(done_tasks) < len(tasks):
        
    for task in tasks_with_time:
        if tasks_with_time[task] == elapsed_seconds:
            done_tasks.append(task)
            
            worker_id = -1
            for w in workers_task:
                if workers_task[w] == task:
                    worker_id = w

            del(workers_task[worker_id])


    for i in range(0, number_of_workers):
        if i not in workers_task: #worker is available
            task = get_next_available_task(tasks, done_tasks, unavailable_tasks)
            if task != None:
                tasks_with_time[task] = elapsed_seconds + get_seconds(task)
                print("Task " + task + " started at " + str(elapsed_seconds) + ". Finishes at " + str(tasks_with_time[task]) + " (worker: " + str(i) + ")")
                workers_task[i] = task
                unavailable_tasks.append(task)

    if len(done_tasks) < len(tasks):
        elapsed_seconds += 1

if debug_output:
    print(tasks_with_time)
    print(unavailable_tasks)
    print(done_tasks)

print(elapsed_seconds)