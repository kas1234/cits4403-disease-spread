"""
Parameter sweep across topology x vaccination strategy x transmission
probability, with multiple stochastic replications per setting.
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
    Returns a long-form DataFrame with one row per replication, ready for
    grouping/plotting (e.g. df.groupby(['topology','strategy','beta']).mean()).
    """
    rows = []
    combos = list(itertools.product(topologies, strategies, betas))

    for topology, strategy, beta in tqdm(combos, desc="sweep"):
        for rep in range(n_replications):
            seed = base_seed + rep
            graph = build_network(topology, n, avg_degree, seed=seed)
            vaccinated = get_vaccinated_set(strategy, graph, budget, seed=seed)
            result = run_sir(graph, beta=beta, gamma=gamma,
                              vaccinated=vaccinated, seed=seed)
            rows.append({
                "topology": topology,
                "strategy": strategy,
                "beta": beta,
                "replication": rep,
                "final_size": result["final_size"],
                "peak_infected": result["peak_infected"],
                "time_to_peak": result["time_to_peak"],
                "duration": result["duration"],
            })

    return pd.DataFrame(rows)
