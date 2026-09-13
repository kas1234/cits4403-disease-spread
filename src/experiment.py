"""
Run the SIR model for different network types, vaccination strategies,
and transmission rates. Each combination is tested multiple times
because the model is stochastic.
"""

import itertools
import pandas as pd
from tqdm import tqdm

from .networks import build_network
from .vaccination import get_vaccinated_set
from .sir_model import run_sir


def run_sweep(topologies: list[str], strategies: list[str], betas: list[float],
              n: int = 300, avg_degree: float = 6, gamma: float = 0.1,
              budget: float = 0.1, n_replications: int = 20,
              base_seed: int = 0) -> pd.DataFrame:
    """
    Runs the SIR simulation for every combination of network,
    vaccination strategy, and transmission probability.

    The results from each replication are stored in a DataFrame
    so they can be easily analysed or plotted later.
    """

    results = []

    # Create all possible combinations of the three parameters
    combinations = list(itertools.product(topologies, strategies, betas))

    for topology, strategy, beta in tqdm(combinations, desc="Running simulations"):

        # Run the same setup several times because each simulation
        # can produce slightly different results
        for replication in range(n_replications):

            seed = base_seed + replication

            # Create the network
            graph = build_network(
                topology,
                n,
                avg_degree,
                seed=seed
            )

            # Select which nodes should be vaccinated
            vaccinated = get_vaccinated_set(
                strategy,
                graph,
                budget,
                seed=seed
            )

            # Run the SIR simulation
            result = run_sir(
                graph,
                beta=beta,
                gamma=gamma,
                vaccinated=vaccinated,
                seed=seed
            )

            # Save the important results from this simulation
            results.append({
                "topology": topology,
                "strategy": strategy,
                "beta": beta,
                "replication": replication,
                "final_size": result["final_size"],
                "peak_infected": result["peak_infected"],
                "time_to_peak": result["time_to_peak"],
                "duration": result["duration"]
            })

    # Convert all simulation results into a DataFrame
    return pd.DataFrame(results)
