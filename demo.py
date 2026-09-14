"""
Simple test of the SIR model.

This file creates one network, applies a vaccination strategy,
runs the infection simulation, and then plots the results.
It can be used to check that everything is working before
running the larger experiment.
"""

from src.networks import build_network
from src.vaccination import get_vaccinated_set
from src.sir_model import run_sir
from src.visualize import plot_epidemic_curve


if __name__ == "__main__":

    # Basic settings for the simulation
    N = 300
    AVG_DEGREE = 6

    # Infection and recovery probabilities
    BETA = 0.08
    GAMMA = 0.1

    # Vaccination settings
    STRATEGY = "degree"
    BUDGET = 0.1

    # Use a fixed seed so the results can be reproduced
    SEED = 42

    # Create the network
    graph = build_network(
        "scale_free",
        N,
        AVG_DEGREE,
        seed=SEED
    )

    # Choose which nodes will be vaccinated
    vaccinated = get_vaccinated_set(
        STRATEGY,
        graph,
        BUDGET,
        seed=SEED
    )

    # Run the SIR simulation
    result = run_sir(
        graph,
        beta=BETA,
        gamma=GAMMA,
        vaccinated=vaccinated,
        seed=SEED
    )

    # Display the main results
    print(
        f"Final outbreak size: "
        f"{result['final_size']:.1%} of population"
    )

    print(f"Peak infected: {result['peak_infected']}")
    print(f"Time to peak: {result['time_to_peak']}")
    print(f"Outbreak duration: {result['duration']} timesteps")

    # Create and save the epidemic curve
    plot_epidemic_curve(
        result,
        title=f"SIR on scale-free network "
              f"({STRATEGY} vaccination, beta={BETA})",
        save_path="results/demo_epidemic_curve.png"
    )

    print("\nSaved plot to results/demo_epidemic_curve.png")
