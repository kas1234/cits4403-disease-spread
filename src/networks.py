"""
Functions for creating different types of networks.

Each network is created with a similar average number of connections
so that we can compare the effect of the network structure fairly.
"""

import networkx as nx


def make_random(n: int, avg_degree: float, seed: int | None = None) -> nx.Graph:
    """Create a random Erdos-Renyi network."""
    
    # Calculate the probability of creating an edge
    probability = avg_degree / (n - 1)

    return nx.erdos_renyi_graph(
        n,
        probability,
        seed=seed
    )


def make_small_world(n: int, avg_degree: int, beta: float = 0.1,
                     seed: int | None = None) -> nx.Graph:
    """Create a Watts-Strogatz small-world network."""

    # The number of neighbours needs to be even
    k = int(avg_degree)

    if k % 2 != 0:
        k += 1

    return nx.watts_strogatz_graph(
        n,
        k,
        beta,
        seed=seed
    )


def make_scale_free(n: int, avg_degree: int,
                    seed: int | None = None) -> nx.Graph:
    """Create a Barabasi-Albert scale-free network."""

    # Number of connections each new node makes
    m = max(1, int(avg_degree // 2))

    return nx.barabasi_albert_graph(
        n,
        m,
        seed=seed
    )


# Store all the network types in one dictionary
TOPOLOGIES = {
    "random": make_random,
    "small_world": make_small_world,
    "scale_free": make_scale_free
}


def build_network(topology: str, n: int, avg_degree: float,
                  seed: int | None = None) -> nx.Graph:
    """Build a network based on the selected topology."""

    if topology not in TOPOLOGIES:
        raise ValueError(
            f"Unknown topology '{topology}'. "
            f"Choose from: {list(TOPOLOGIES)}"
        )

    return TOPOLOGIES[topology](n, avg_degree, seed=seed)
