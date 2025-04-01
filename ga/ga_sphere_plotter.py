import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def plot_sphere_function(filename="sphere_ga_evolution.csv"):
 
    """
    Plots the evolution progress of a genetic algorithm optimizing the Sphere function.
    
    Parameters:
    filename (str): The CSV file containing generation, x, y, and fitness data.
    """
    try:
        # Load the data with correct column names
        data = pd.read_csv(filename, names=["Generation", "x", "y", "Fitness"], skiprows=1)

        # Create a mesh grid for the Sphere function
        x_vals = np.linspace(-10, 10, 100)
        y_vals = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = X**2 + Y**2  # Sphere function f(x, y) = x^2 + y^2

        # Create figure
        fig = go.Figure()

        # **Green Sphere function surface**
        fig.add_trace(go.Surface(
            z=Z, x=X, y=Y, 
            colorscale=[(0, "darkgreen"), (1, "lightgreen")], 
            opacity=0.8, 
            name="Sphere Function"
        ))

        # **Blue evolution dots**
        fig.add_trace(go.Scatter3d(
            x=data["x"], y=data["y"], z=data["Fitness"],
            mode="markers+lines",
            marker=dict(size=5, color="blue", opacity=1),
            line=dict(width=2, color="blue"),
            name="Evolution Path"
        ))

        # **Scientific layout settings**
        fig.update_layout(
            title="Genetic Algorithm Optimization of Sphere Function",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Fitness (x² + y²)",
                xaxis=dict(showgrid=True, gridcolor="lightgray"),
                yaxis=dict(showgrid=True, gridcolor="lightgray"),
                zaxis=dict(showgrid=True, gridcolor="lightgray"),
            ),
            template="plotly_white",
            font=dict(size=14),
            width=900, height=700
        )

        # Show the interactive plot
        fig.show()

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Ensure the data file exists.")
    except Exception as e:
        print(f"An error occurred: {e}")


def sphere_plotter_2d():
        # Load the data and specify column names explicitly
    data = pd.read_csv('sphere_ga_evolution.csv', names=["Generation", "x", "y", "Fitness"], skiprows=1)

    # Plot x, y, and fitness over generations
    plt.figure(figsize=(10,6))

    # Plot x and y
    plt.subplot(2, 1, 1)
    plt.plot(data['Generation'], data['x'], label="x", color="blue")
    plt.plot(data['Generation'], data['y'], label="y", color="green")
    plt.title("X and Y over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Value")
    plt.legend()

    # Plot fitness
    plt.subplot(2, 1, 2)
    plt.plot(data['Generation'], data['Fitness'], label="Fitness", color="red")
    plt.title("Fitness over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
def main():
    plot_sphere_function()
    sphere_plotter_2d()
if __name__ == "__main__":
    main()