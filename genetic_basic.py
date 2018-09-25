import random
import math

x_min = 1.000000000000001
y_min = 1.000000000000001
x_max = 9.999999999999999
y_max = 9.999999999999999
popsize = 10
target = -5 #100.0 ## Change between 100 and -5 for Question 3
num_gen = 300

# Creates a population of size n with initial fitness infinity
def gen_pop(n):
    return [(random.uniform(x_min, x_max), random.uniform(y_min, y_max), float('inf')) for i in range(n)]

# Finding the z value
def zval(x, y): 
    return math.pow(x, 2) + math.exp(y / 5) + 100 * math.log(x, 2) - 1 / (x * y) - x

# Calculates the fitness of z
def fitness(zval):
    return abs(zval - target)

# Merges the population with fitness 
def run_gen(pop):
    return [(p[0], p[1], fitness(zval(p[0], p[1]))) for p in pop]

# Sorts the population and returns the top half (best half)
def pick_toppers(pop, size):
    sortedpop = sorted(pop, key=lambda x: x[2])
    return sortedpop[:size]

# Randomly selects a x and y values and deviates it by 10%
def mutate(pop):
    xchoice = random.randint(0, 9)
    E = random.uniform(-0.1, 0.1)
    # change pop[xchoice][0] by 1+E
    new_x = pop[xchoice][0]*(1+E)
    pop[:xchoice] + [new_x, pop[xchoice][1], pop[xchoice][2]] + pop[xchoice+1:]

    ychoice = random.randint(0, 9)
    E = random.uniform(-0.1, 0.1)
    # change pop[ychoice][0] by 1+E
    new_y = pop[ychoice][1]*(1+E)
    pop[:ychoice] + [pop[ychoice][0], new_y, pop[ychoice][2]] + pop[ychoice+1:]

    return pop

def crossover(pop):
    # selecting a x and y from two random tuples
    xchoice = random.randint(0, 9)
    ychoice = random.randint(0, 9)
    
    new_x = pop[ychoice][1]
    new_y = pop[xchoice][0]

    # Crossing over x of a random tuple with y of a random tuple
    pop[:xchoice] + [new_x, pop[xchoice][1], pop[xchoice][2]] + pop[xchoice+1:]
    pop[:ychoice] + [pop[ychoice][0], new_y, pop[ychoice][2]] + pop[ychoice+1:]

    return pop

# Runs the GA
def run(initial_pop):
    next_gen = initial_pop

    for i in range(num_gen):
        pop_with_fitness = run_gen(next_gen)
        
        # 20% of the iterations will undergo mutation or crossover
        if random.uniform(0, 1) <= 0.2:             
            # Randomizes mutation or crossover.
            if random.randint(0, 2) == 0:
                for _ in range(5):
                    mutate(pop_with_fitness) 
            else :
                for _ in range(5):
                    crossover(pop_with_fitness) 
        
        if i%150 == 0:      # Change for display interval ########
            stats(i, next_gen)
        toppers = pick_toppers(pop_with_fitness, popsize // 2)
        next_gen = toppers  # Selecting only the best half
        
        # Creating the second half of new population
        next_gen += gen_pop(popsize // 2) 
    return next_gen

def stats(gencount, pop):
    print("\nCurrent Generation : ", gencount)
    print("Population")
    for p in pop:
        print(p)

def main():
    initial_pop = gen_pop(popsize)
    final = run(initial_pop)
    print("\nFinal generation Output")
    print("Total Generations = ", num_gen)
    print("\n".join([str(f) for f in final]))  
    print("\nBest x and y such that z is closest to ", target, 
        " is \n x = ", final[0][0], 
        " and \n y = ", final[0][1],
        " \n with a deviation from z of = ", final[0][2])

if __name__=='__main__':
    main()