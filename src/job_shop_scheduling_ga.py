# Name: Masa Ahamd Ali Jalamneh
# ID: 1212145
# Section: 2

import random
import copy

#---------------------------------- Input section -----------------------------------#
# let user enter number of Jobs
print("Enter number of Jobs:") 
max_jobs = int(input())
 
# let user enter number of machines
print("Enter number of Machines:") 
max_machines = int(input())

# split each line in the input into needed data (job number, machines, required time for each task....)
# and define the jobs list
jobs = {}        
print("Enter Jobs data in the format -> 'job_number: task1 -> task2 -> ...' :")
while True: 
    line = input().strip() # read lines
    if line == '':         # end of jobs
        break   

    try:
        job_number, tasks_str = line.split(': ')  
        job_num = int(job_number.split('_')[1])  # get Job number
        tasks = tasks_str.split(' -> ')          # get Job tasks
        job_tasks = []  

        for seq_num, task in enumerate(tasks, start=1):
            try:
                machine, time = task.split('[')
                m_num = int(machine[1:])
                time = int(time[:-1])  # Remove the closing bracket and convert to int
                job_tasks.append((m_num, time))

            except ValueError as e:
                print(f"Error processing task '{task}' in job '{job_number}': {e}")
        jobs[job_num] = job_tasks 

    except ValueError:
        print("Invalid format!! Please use the format 'job_number: task1 -> task2 -> ...'")

# print as output the jobs data
#for job_num, job_tasks in jobs.items():
#    print(f"Job {job_num}: {job_tasks}")

#---------------------------------- Functions section -----------------------------------#
# chromosomes generator function
def generate_chromosome():
    chromosome = []
    machine_schedules = {i: [] for i in range(1, max_machines + 1)}  # to keep track on schedules for each machine to avoid conflects  

    for job_num, job_tasks in jobs.items():
        tasks_start_times = [0] * (max_machines + 1) # starting time for task where every element is initially set to 0
        #print(f"--Job {job_num}--") # to show tasks scheduling for each job 

        for task_index, (m_num, time) in enumerate(job_tasks):
            start_time = max(tasks_start_times[m_num], tasks_start_times[0])

            # condition to check for machine conflicts and solve if occurred
            while any(start_time < end and start_time + time > start for start, end in machine_schedules[m_num]):
                conflict_occurred_in_tasks = next(
                    (start, end) for start, end in machine_schedules[m_num] if start_time < end and start_time + time > start)
                #print(
                #    f"Conflict detected on Machine {m_num} between times {start_time}-{start_time + time} and existing task {conflict_occurred_in_tasks}. Adjusting start time.")
                start_time = conflict_occurred_in_tasks[1]  # to solve conflict -> shift start time to the end of the conflicting task

            end_time = start_time + time # calculate end time for each task
            # printing assigned data (task number, machine number, srarting time and ending time)
            #print(f"Task {task_index + 1} for Machine {m_num}:")
            #print(f"Scheduled Start Time: {start_time}, End Time: {end_time}")

            # add task to job schedule and machine schedule
            chromosome.append((job_num, m_num, start_time, end_time))
            machine_schedules[m_num].append((start_time, end_time)) # to print the program schedule at the end of the program
            machine_schedules[m_num].sort()  # to make sure that  machine schedules are sorted by start time

            # for sequential tasks in the same job i had to update start times each time 
            tasks_start_times[m_num] = end_time
            tasks_start_times[0] = end_time  # to mach sure tasks are in sequential order within the job

        #print()  

    return chromosome

# initialize and generate a random population of schedules
def initialize_population(p_size):
    population = []
    for _ in range(p_size):

        chromosome = generate_chromosome()
        random.shuffle(chromosome)  
        population.append(chromosome) # append chromosomes

    return population 

# this function is to evaluate the total time for the schedule
def fitness(chromosome):
    end_times = [0] * (max_machines + 1)
    job_end_times = [0] * (max_jobs + 1)
    machine_schedules = [[] for _ in range(max_machines + 1)]

    for job_num, m_num, start_time, time in chromosome:
        actual_start_time = max(job_end_times[job_num], end_times[m_num])
        end_time = actual_start_time + time
        machine_schedules[m_num].append((job_num, actual_start_time, end_time))
        job_end_times[job_num] = end_time
        end_times[m_num] = end_time

    return max(end_times) # end time for last task in the program 

# Select parents function by using tournament selection 
def tournament_selection(population, k):
    selected_parents = []

    for _ in range(k):
        sample = random.sample(population, 2)
        fitnesses = [fitness(chromosome) for chromosome in sample]
        selected_parents.append(sample[fitnesses.index(min(fitnesses))])

    return selected_parents

# crossover function where it should combine two parent (at a certain position) to create children
def crossover(parent1, parent2):
    size = len(parent1)
    crossover_position = random.randint(1, size - 1) # find the certain position to do the crossover

    child1 = parent1[:crossover_position] + [task for task in parent2 if task not in parent1[:crossover_position]]
    child2 = parent2[:crossover_position] + [task for task in parent1 if task not in parent2[:crossover_position]]
    return child1, child2

# mutation function to arbitrary change in a situation and to prevent the algorithm from getting stuck
def mutation(chromosome, mutation_rate):
    chosen_chromosome = copy.deepcopy(chromosome) # chose a chromosome to do mutation

    for i in range(len(chosen_chromosome)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(chosen_chromosome) - 1)
            chosen_chromosome[i], chosen_chromosome[j] = chosen_chromosome[j], chosen_chromosome[i]

    return chosen_chromosome

#---------------------------------- Calling functions and printing results section -----------------------------------#
# ----------------------------
population_size = 100
num_generations = 100
mutation_rate = 0.1
# ----------------------------

# call the genetic algorithm functions (population initializer, selection, crossover, mutation)
population = initialize_population(population_size)
for generation in range(num_generations):
    new_population = []
    
    for _ in range(population_size // 2):
        # parents selection
        parents = tournament_selection(population, 2) # select parents by calling the function

        # parents crossover
        child_1, child_2 = crossover(parents[0], parents[1])
    
        # mutation procedure if needed 
        new_population.append(mutation(child_1, mutation_rate))
        new_population.append(mutation(child_2, mutation_rate))

    population = new_population 


# chromosome generation 
chromosome = generate_chromosome()

total_production_time = 0  # total time for all processes from the first task till the last one  

# printing the result which is a schedule that include job number, machine number, start time and end time
print("Best Schedule:")
print("Job\tMachine\t Start\tEnd")
for job_num, m_num, start_time, end_time in sorted(chromosome, key=lambda x: (x[2], x[1])):
    print(f"{job_num}\tM{m_num}\t {start_time}\t{end_time}")
total_production_time = max(total_production_time, end_time)

print(f"\nTotal Production Time: {total_production_time}") # print the total time needed

#---------------------------------------- End of program ------------------------------------------#