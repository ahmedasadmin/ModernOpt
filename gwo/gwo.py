import random 
import math
import copy 
import sys
import numpy as np
import  matplotlib.pyplot as plt
import plotly.graph_objects as go

#---------------fitness functions----------
#
#
# rastringin function

# rastrigin function 
def fitness_rastrigin(position): 
  fitness_value = 0.0
  for i in range(len(position)): 
    xi = position[i] 
    fitness_value += (xi * xi) - (10 * math.cos(2 * math.pi * xi)) + 10
  return fitness_value 
  
#-------------------------------------------
#sphere function
def fitness_sphere(position):
    fitness_value = 0.0
    for i in range(len(position)):
        xi = position[i]
        fitness_value += (xi * xi);
    return fitness_value
#---------------------------------------------

class wolf:
    def __init__(self, fitness, dim, minx, maxx, seed):
        self.position  = [0.0 for i in range(dim)]
        self.rnd = random.Random(seed)
        for i in range(dim):
            self.position[i] = ((maxx - minx) * self.rnd.random() + minx)

        self.fitness = fitness(self.position)
def gwo(fitness, max_iter, n, dim, minx, maxx):
    rnd = random.Random(0)

    # Create n random wolves
    population = [wolf(fitness, dim, minx, maxx, i) for i in range(n)] 

    # Sort population by fitness
    population = sorted(population, key=lambda temp: temp.fitness)
    alpha_wolf, beta_wolf, gamma_wolf = population[0], population[1], population[2]
    best_fitness_over_time =  []                  # store best fitness per iteration

    Iter = 0
    while Iter < max_iter:
        if Iter % 10 == 0:
            print("Iter =", Iter, "best fitness = %.6f" % alpha_wolf.fitness)
            best_fitness_over_time.append(alpha_wolf.fitness)
        a = 2 * (1 - Iter / max_iter)  # Linearly decreasing a

        for i in range(n):
            A1, A2, A3 = a * (2 * rnd.random() - 1), a * (2 * rnd.random() - 1), a * (2 * rnd.random() - 1)
            C1, C2, C3 = 2 * rnd.random(), 2 * rnd.random(), 2 * rnd.random()

            X1 = [alpha_wolf.position[j] - A1 * abs(C1 * alpha_wolf.position[j] - population[i].position[j]) for j in range(dim)]
            X2 = [beta_wolf.position[j] - A2 * abs(C2 * beta_wolf.position[j] - population[i].position[j]) for j in range(dim)]
            X3 = [gamma_wolf.position[j] - A3 * abs(C3 * gamma_wolf.position[j] - population[i].position[j]) for j in range(dim)]
            
            Xnew = [(X1[j] + X2[j] + X3[j]) / 3.0 for j in range(dim)]  
            for j in range(dim):
                Xnew[j] = min(max(Xnew[j], minx), maxx)
            fnew = fitness(Xnew)

            if fnew < population[i].fitness:  # Greedy selection
                population[i].position = Xnew[:]
                population[i].fitness = fnew

        # Re-sort population
        population = sorted(population, key=lambda temp: temp.fitness)
        alpha_wolf, beta_wolf, gamma_wolf = population[0], population[1], population[2]

        Iter += 1

    return alpha_wolf.position, best_fitness_over_time  # Return best position

#----------------------------------
def plot_fitness_convergence(best_fitness_over_time):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 11), best_fitness_over_time[:10], marker="o", linestyle="-", color="b")
    plt.xticks(range(1, 11))
    plt.xlabel("Iteration")
    plt.ylabel("Best Fitness Value")
    plt.title("GWO Convergence Over Iterations")
    plt.grid()
    plt.show()

#----------------------------------
def plot_rastrigin_3d(best_position):
    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)

    Z = (X**2 - 10 * np.cos(2 * np.pi * X) + 10) + (Y**2 - 10 * np.cos(2 * np.pi * Y) + 10)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

    # Mark the best position found
    ax.scatter(best_position[0], best_position[1], fitness_rastrigin(best_position[:2]), color="r", s=100, label="Best Solution")
    ax.set_xlabel("X1")
    ax.set_ylabel("X2")
    ax.set_zlabel("Fitness Value")
    ax.set_title("GWO on Rastrigin Function")
    ax.legend()
    plt.show()

def plot_rastrigin_3d_interactive(best_position):
    X = np.linspace(-5.12, 5.12, 100)
    Y = np.linspace(-5.12, 5.12, 100)
    X, Y = np.meshgrid(X, Y)
    Z = (X**2 - 10 * np.cos(2 * np.pi * X) + 10) + (Y**2 - 10 * np.cos(2 * np.pi * Y) + 10)

    fig = go.Figure()

    # Add surface plot
    fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="viridis", opacity=0.7))

    # Add best solution point
    fig.add_trace(go.Scatter3d(
        x=[best_position[0]], y=[best_position[1]], z=[fitness_rastrigin(best_position[:2])],
        mode="markers",
        marker=dict(size=8, color="red"),
        name="Best Solution"
    ))

    fig.update_layout(
        title="GWO on Rastrigin Function",
        scene=dict(
            xaxis_title="X1",
            yaxis_title="X2",
            zaxis_title="Fitness Value"
        )
    )

    fig.show()
#-----------------------------------
def main():

    # Drive code for rastrigin objective function
    print("\nBegin the  Grey Wolf Optimization on rastringin function\n")
    dim = 3
    fitness = fitness_rastrigin
    print("Goal is to minimize Rastrigin's function in " + str(dim) + " variables")
    print("Function has known min = 0.0 at (", end="")
    for i in range(dim-1):
        print("0, ", end="")
    print("0)")

    num_particles = 50
    max_iter = 100

    print("Setting num_particles = " + str(num_particles))
    print("Setting max_iter      = " + str(max_iter))
    print("\nStarting GWO algorithm\n")


    best_position, best_fitness_over_time = gwo(fitness, max_iter, num_particles, dim, -10.0, 10.0)
    plot_rastrigin_3d(best_position)
    plot_rastrigin_3d_interactive(best_position)
    plot_fitness_convergence(best_fitness_over_time)
    print("\nGWO completed\n")
    print("\nBest solution found:")
    print(["%.6f"%best_position[k] for k in range(dim)])
    err = fitness(best_position)
    print("fitness of best solution = %.6f" %err)

    print("\nEnd GWO for rastrigin\n")


if __name__ == "__main__":
    main()