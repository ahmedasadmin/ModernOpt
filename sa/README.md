# Simulated Annealing for Function Minimization

This Python script uses the **Simulated Annealing** algorithm to minimize a simple quadratic function \( f(x) = x^2 \). The script starts from an initial state, searches for the minimum, and visually shows the optimization process.

## Overview

Simulated Annealing (SA) is a probabilistic technique used for finding the global minimum of a function. It is inspired by the process of annealing in metallurgy, where material is heated and then slowly cooled to remove defects in the structure.

In this implementation, we use the SA algorithm to minimize the quadratic function \( f(x) = x^2 \), starting from a random initial state (default: x = 10).

## Functionality

1. **Objective Function**: The function to minimize is \( f(x) = x^2 \).
2. **Optimization Process**: 
   - Starts at an initial state (default: 10.0)
   - Generates new states by adding small random perturbations
   - Accepts better states always and worse states probabilistically based on temperature
3. **Cooling Schedule**: The temperature decreases geometrically (default rate: 0.99) after each iteration
4. **Visualization**: Generates two plots:
   - State (x) vs. iteration
   - Function value (f(x)) vs. iteration

## Requirements

- Python 3.x
- NumPy
- Matplotlib

Install the required libraries using pip:

```bash
pip install numpy matplotlib