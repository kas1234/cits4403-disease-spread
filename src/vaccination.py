"""
Vaccination strategies.

Each strategy takes a graph and a budget (fraction of nodes to vaccinate)
and returns the *set* of node ids to vaccinate. Vaccinated nodes are treated
as immune (Recovered) from t=0, i.e. removed from the susceptible pool
before the outbreak is seeded.
"""

import random
import networkx as nx


def vaccinate_random(graph: nx.Graph, budget: float, seed: int | None = None) -> set:
    rng = random.Random(seed)
    n_vacc = int(round(budget * graph.number_of_nodes()))
    return set(rng.sample(list(graph.nodes()), n_vacc))


def vaccinate_by_degree(graph: nx.Graph, budget: float, seed: int | None = None) -> set:
    """Vaccinate the highest-degree nodes first (targets hubs)."""
    n_vacc = int(round(budget * graph.number_of_nodes()))
    ranked = sorted(graph.degree, key=lambda x: x[1], reverse=True)
    return {node for node, _ in ranked[:n_vacc]}


def vaccinate_by_betweenness(graph: nx.Graph, budget: float, seed: int | None = None) -> set:
    """Vaccinate the highest-betweenness-centrality nodes first (targets bridges).

    Note: betweenness centrality is O(n * m) — fine for a few hundred/thousand
    nodes, but if your experiments get slow, switch to the `k` sampling
    parameter of nx.betweenness_centrality (approximate but much faster).
    """
    n_vacc = int(round(budget * graph.number_of_nodes()))
    centrality = nx.betweenness_centrality(graph, seed=seed)
    ranked = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    return {node for node, _ in ranked[:n_vacc]}


STRATEGIES = {
    "random": vaccinate_random,
    "degree": vaccinate_by_degree,
    "betweenness": vaccinate_by_betweenness,
    "none": lambda graph, budget, seed=None: set(),
}


def get_vaccinated_set(strategy: str, graph: nx.Graph, budget: float,
                        seed: int | None = None) -> set:
    if strategy not in STRATEGIES:
        raise ValueError(f"Unknown strategy '{strategy}'. Options: {list(STRATEGIES)}")
    return STRATEGIES[strategy](graph, budget, seed=seed)
