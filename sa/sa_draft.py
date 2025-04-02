import numpy as np
import math 
import random
import matplotlib.pyplot as plt


def func(x):
    """
    A simple quadratic function f(x) = x^2, which we want to minimize.
    
    Args:
    - x (float): the input value to the function 
    
    Returns:
    - float: the value at x.
    """

    return x*x

# Simulated Annealing algorithm to minimize

def simulated_annealing(func, initial_state, temperature, cooling_rate,max_itrations):
    """
    Optimizes a function using the simulated Annealing algorithm.

    Args:
    - func (function): The function to minimize (should take one argument).
    - initial_state (float): The starting point for optimization.
    - temperature (float): the initial temperature for annealing process.
    - cooling (float): The rate at which the temperature cools down after each iteration.
    - max_iterations: The maximum number of iterations to perform.

    Returns:
    - final_state (float): The state at which the function reach its minimum.
    - final_value (float: The function value at the final state.
    - history (list): A list of states and function values throughout the optimization process.
    """
    current_state = initial_state
    current_value = func(initial_state)
    history = [(current_state, current_value)]
    
    for iteration in range(max_itrations):
        # Generate a new state by making a small random change to the current state
        new_state = current_state + np.random.uniform(-1, 1)
        new_value = func(new_state)

        # calulate the change in value 
        delta = new_value - current_state
        # if the new state is better (lower value), accept it 
        if delta < 0:
            current_state = new_state
            current_value = new_value
        # If the new state is worse (higher value), accept it with a certain probability
        else:
            # Probability of accepting a worse state decreases as temperature decreases
            probability = math.exp(-delta / temperature)
            if random.random() < probability:
                current_state = new_state
                current_value = new_value

        # Cool down the temperature to reduce the likelihood of accepting worse states 
        temperature *= cooling_rate

        #Store the state and function value history
        history.append((current_state, current_value))
    
    return current_state, current_value, history

# Parameters for the optimzation process
initial_state = 5
initial_temperature = 100
cooling_rate = 0.99
max_iterations = 1000


# Run simualted annealing
final_state, final_value, history = simulated_annealing(func, initial_state, initial_temperature, cooling_rate, max_iterations)

print(f"[DONE] optimal State: {final_state} with Optimal value: {final_value}")

x_vals = [state for state, _ in history]
y_vals = [value for _, value in history]

plt.plot(x_vals, y_vals)
plt.xlabel("State (x)")
plt.ylabel("Function value (f(x))")
plt.title("Simulate Annealing Optimization")
plt.show()

