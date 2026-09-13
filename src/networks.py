"""
Network topology generators.

Each function returns a networkx.Graph with `n` nodes and roughly comparable
average degree, so that comparisons across topologies are fair (you're
varying *structure*, not just changing how many contacts people have).
"""

import networkx as nx


def make_random(n: int, avg_degree: float, seed: int | None = None) -> nx.Graph:
    """Erdos-Renyi random graph: no structure beyond a fixed edge probability."""
    p = avg_degree / (n - 1)
    return nx.erdos_renyi_graph(n, p, seed=seed)


def make_small_world(n: int, avg_degree: int, beta: float = 0.1,
                      seed: int | None = None) -> nx.Graph:
    """Watts-Strogatz small-world graph: clustered locally, short global paths."""
    k = int(avg_degree)
    if k % 2 != 0:
        k += 1  # watts_strogatz_graph requires even k
    return nx.watts_strogatz_graph(n, k, beta, seed=seed)


def make_scale_free(n: int, avg_degree: int, seed: int | None = None) -> nx.Graph:
    """Barabasi-Albert scale-free graph: a few very high-degree hubs."""
    m = max(1, int(avg_degree // 2))
    return nx.barabasi_albert_graph(n, m, seed=seed)


TOPOLOGIES = {
    "random": make_random,
    "small_world": make_small_world,
    "scale_free": make_scale_free,
}


def build_network(topology: str, n: int, avg_degree: float,
                   seed: int | None = None) -> nx.Graph:
    if topology not in TOPOLOGIES:
        raise ValueError(f"Unknown topology '{topology}'. Options: {list(TOPOLOGIES)}")
    return TOPOLOGIES[topology](n, avg_degree, seed=seed)
