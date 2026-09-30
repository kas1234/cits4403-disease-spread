"""
Full parameter sweep: network topology x vaccination strategy x transmission
probability, multiple stochastic replications per combination. This is the
Checkpoint 2 target result comparing how network structure changes which
vaccination strategy works best under a fixed vaccination budget.
"""

import os
from src.experiment import run_sweep
from src.visualize import plot_phase_diagram

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)

    df = run_sweep(
        topologies=["random", "small_world", "scale_free"],
        strategies=["none", "random", "degree", "betweenness"],
        betas=[0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20],
        n=300,
        avg_degree=6,
        gamma=0.1,
        budget=0.1,
        n_replications=15,
        base_seed=0,
    )

    df.to_csv("results/sweep_results.csv", index=False)
    print(f"Saved {len(df)} rows to results/sweep_results.csv")

    plot_phase_diagram(df, metric="final_size", save_path="results/phase_diagram_final_size.png")
    print("Saved results/phase_diagram_final_size.png")

    plot_phase_diagram(df, metric="peak_infected", save_path="results/phase_diagram_peak_infected.png")
    print("Saved results/phase_diagram_peak_infected.png")
