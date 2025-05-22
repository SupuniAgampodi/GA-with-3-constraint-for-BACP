import json
import random
import datetime
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Genetic Algorithm Parameters
population_size = 100
generations = 300
tournament_size = 10
crossover_probability = 0.9
mutation_probability = 0.1

# Read file
json_file = input(
    "Enter the name of the json file:"
    "\n 1- MJ-IAID.json"
    "\n 1- MJ-IAID.json"
    "\n4- bacp08.json"
    "\n5- bacp10.json"
    "\n6- bacp12.json\n")

with open(json_file) as f:
    data = json.load(f)
    units = data['units']
    prerequisites = data['prerequisites']
    parameters = data['parameters']

total_semesters = parameters.get("Total_Semesters")
min_credits_sem = parameters.get("Min_Credits_Sem")
max_credits_sem = parameters.get("Max_Credits_Sem")
min_units_sem = parameters.get("Min_Units_Sem")
max_units_sem = parameters.get("Max_Units_Sem")

# Fitness Function
def Fitness(individual):
    availability_violations = 0
    prerequisite_violations = 0
    credit_violations = 0
    course_violations = 0
    credits_per_semester = [0] * total_semesters
    units_per_semester = [0] * total_semesters
    unit_schedule = {}

    for i, gene in enumerate(individual):
        unit = list(units.keys())[i]
        semester = gene
        credits_per_semester[semester - 1] += units[unit]['credits']
        units_per_semester[semester - 1] += 1
        unit_schedule[unit] = semester

        # Constraint 1 - Checking Semester Availability
        if semester not in units[unit]['available']:
            availability_violations += 1

    # Constraint 2 - Checking Prerequisite Requirements
    for unit, prereqs in prerequisites.items():
        if unit in unit_schedule:
            unit_semester = unit_schedule[unit]
            for prereq in prereqs:
                if prereq in unit_schedule:
                    prereq_semester = unit_schedule[prereq]
                    if prereq_semester >= unit_semester:
                        prerequisite_violations += 1

    # Constraint 3 - Checking Credit Limit Requirements
    for credits in credits_per_semester:
        if credits < min_credits_sem or credits > max_credits_sem:
            credit_violations += 1

    # Constraint 4 - Checking Course Limit Requirements
    for units_count in units_per_semester:
        if units_count < min_units_sem or units_count > max_units_sem:
            course_violations += 1

    # Main objective: minimize maximum credit load
    max_credit_load = max(credits_per_semester)


    return (availability_violations + prerequisite_violations
            + credit_violations + course_violations + max_credit_load),

# Mutation Operator
def Mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_probability:
            unit = list(units.keys())[i]
            available_semesters = units[unit]['available']
            individual[i] = random.choice(available_semesters)
    return individual,


# DEAP Setup
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("attr_gene", lambda: random.choice(range(1, total_semesters + 1)))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_gene, n=len(units))
toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=population_size)
toolbox.register("evaluate", Fitness)
toolbox.register("select", tools.selTournament, tournsize=tournament_size)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", Mutate)



# Run Genetic Algorithm
def main():
    population = toolbox.population()
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)

    logbook = tools.Logbook()
    logbook.header = ["gen", "nevals", "avg", "min", "max"]

    for gen in range(generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=crossover_probability, mutpb=mutation_probability)
        fits = list(map(toolbox.evaluate, offspring))
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))
        hof.update(population)
        record = stats.compile(population)
        logbook.record(gen=gen, nevals=len(offspring), **record)

    return hof[0], logbook


# Run the GA 10 times and Record
all_logbooks = []
best_fitnesses = []
avg_fitnesses = []
max_fitnesses = []
execution_times = []
best_individuals = []


now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")
json_basename = os.path.splitext(os.path.basename(json_file))[0]
results_dir = "results"
os.makedirs(results_dir, exist_ok=True)
save_filename = os.path.join(results_dir, f"results_(PS{population_size}_CP{crossover_probability}_MP{mutation_probability}_GN{generations})_{json_basename}_{timestamp}")

def decode_schedule(individual):
    schedule = {i: [] for i in range(1, total_semesters + 1)}
    for i, semester in enumerate(individual):
        unit = list(units.keys())[i]
        schedule[semester].append(unit)
    return schedule


def calculate_minmax_balance(individual):
    credits_per_semester = [0] * total_semesters
    for i, semester in enumerate(individual):
        unit = list(units.keys())[i]
        credits_per_semester[semester - 1] += units[unit]['credits']

    minmax = max(credits_per_semester)
    balance = np.std(credits_per_semester)

    return minmax, balance



with open(f"{save_filename}.txt", "w") as f:

    f.write(f"{'Population Size:':<30}{population_size:.2f}\n")
    f.write(f"{'Crossover Probability:':<30}{crossover_probability:.2f}\n")
    f.write(f"{'Mutation Probability:':<30}{mutation_probability:.2f}\n")
    f.write(f"{'Generations':<30}{generations:.2f}\n")
    f.write("\n" + "=" * 100 + "\n")

    f.write(
        f"{'Run':<5}{'Avg Fitness':<20}{'Best Fitness':<20}{'Worst Fitness':<20}{'Exec Time (s)':<15}{'MinMax':<10}{'Balance':<10}\n")
    f.write("-" * 100 + "\n")

    all_avg = []
    all_min = []
    all_max = []
    all_times = []
    all_minmax = []
    all_balance = []

    for run in range(1, 11):
        print(f"\n=== Run {run} ===\n")
        start_time = time.time()

        best, logbook = main()

        all_logbooks.append(logbook)

        end_time = time.time()
        exec_time = end_time - start_time

        gen_avg = logbook.select("avg")
        gen_min = logbook.select("min")
        gen_max = logbook.select("max")

        # Compute stats across all generations of this run
        run_avg_fitness = np.mean(gen_avg)
        run_best_fitness = np.min(gen_min)
        run_worst_fitness = np.max(gen_max)
        minmax, balance = calculate_minmax_balance(best)

        all_avg.append(run_avg_fitness)
        all_min.append(run_best_fitness)
        all_max.append(run_worst_fitness)
        all_times.append(exec_time)
        all_minmax.append(minmax)
        all_balance.append(balance)

        f.write(
            f"{run:<5}{run_avg_fitness:<20.2f}{run_best_fitness:<20.2f}{run_worst_fitness:<20.2f}{exec_time:<15.2f}")
        f.write(f"{minmax:<10}{balance:<10.2f}\n")  # <<< NEW

    # Overall statistics across all runs
    overall_avg = np.mean(all_avg)
    overall_best = np.min(all_min)
    overall_worst = np.max(all_max)
    avg_time = np.mean(all_times)
    avg_minmax = np.min(all_minmax)
    avg_balance = np.min(all_balance)

    f.write("\n" + "=" * 100 + "\n")
    f.write(f"{'Overall Avg Fitness:':<30}{overall_avg:.2f}\n")
    f.write(f"{'Overall Best Fitness:':<30}{overall_best:.2f}\n")
    f.write(f"{'Overall Worst Fitness:':<30}{overall_worst:.2f}\n")
    f.write(f"{'Average Execution Time (s):':<30}{avg_time:.2f}\n")
    f.write(f"{'Best MinMax:':<30}{avg_minmax:.2f}\n")
    f.write(f"{'Best Balance:':<30}{avg_balance:.2f}\n")

    f.write("\n" + "=" * 100 + "\n")
    decoded_schedule = decode_schedule(best)
    f.write(f"{decoded_schedule}\n")

print("\nAll runs completed. Results saved to GA_Results.txt")


title_text = f'Convergence Plot (PS={population_size}, CP={crossover_probability}, MP={mutation_probability}, GN={generations})'
save_plot_name = os.path.join(results_dir, f"Convergence_Plot_(PS{population_size}_CP{crossover_probability}_MP{mutation_probability}_GN{generations})_{json_basename}_{timestamp}.jpg")

# Extract statistics
gen = logbook.select("gen")
avg = logbook.select("avg")
min_ = logbook.select("min")
max_ = logbook.select("max")

# Plot the best run
plt.figure(figsize=(10, 6))
plt.plot(gen, avg, label='Average Fitness')
plt.plot(gen, min_, label='Minimum Fitness')
plt.plot(gen, max_, label='Maximum Fitness')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.title('Fitness Evolution Over Generations')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(save_plot_name)
plt.show()


# Decode and print schedule
decoded_schedule = decode_schedule(best)
for semester, units in decoded_schedule.items():
    print(f"Semester {semester}: {', '.join(units)}")