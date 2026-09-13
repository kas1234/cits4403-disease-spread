"""
Different ways of choosing which nodes should be vaccinated.

The budget is the fraction of the total population that can be vaccinated.
Vaccinated nodes are treated as immune before the infection starts.
"""

import random
import networkx as nx


def vaccinate_random(graph: nx.Graph, budget: float,
                     seed: int | None = None) -> set:
    """Randomly choose nodes to vaccinate."""

    rng = random.Random(seed)

    # Work out how many people can be vaccinated
    number_to_vaccinate = int(
        round(budget * graph.number_of_nodes())
    )

    nodes = list(graph.nodes())

    return set(rng.sample(nodes, number_to_vaccinate))


def vaccinate_by_degree(graph: nx.Graph, budget: float,
                        seed: int | None = None) -> set:
    """Vaccinate the nodes with the most connections first."""

    number_to_vaccinate = int(
        round(budget * graph.number_of_nodes())
    )

    # Sort nodes from highest degree to lowest degree
    ranked_nodes = sorted(
        graph.degree,
        key=lambda item: item[1],
        reverse=True
    )

    # Select the nodes with the highest number of connections
    return {
        node for node, degree in ranked_nodes[:number_to_vaccinate]
    }


def vaccinate_by_betweenness(graph: nx.Graph, budget: float,
                             seed: int | None = None) -> set:
    """Vaccinate nodes that are important for connecting different parts
    of the network.
    """

    number_to_vaccinate = int(
        round(budget * graph.number_of_nodes())
    )

    # Calculate how important each node is for connecting the network
    centrality = nx.betweenness_centrality(
        graph,
        seed=seed
    )

    # Sort nodes from highest to lowest betweenness
    ranked_nodes = sorted(
        centrality.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return {
        node for node, centrality_value
        in ranked_nodes[:number_to_vaccinate]
    }


# Match each strategy name with its function
STRATEGIES = {
    "random": vaccinate_random,
    "degree": vaccinate_by_degree,
    "betweenness": vaccinate_by_betweenness,
    "none": lambda graph, budget, seed=None: set()
}


def get_vaccinated_set(strategy: str, graph: nx.Graph,
                       budget: float,
                       seed: int | None = None) -> set:
    """Choose the vaccination strategy requested by the user."""

    if strategy not in STRATEGIES:
        raise ValueError(
            f"Unknown strategy '{strategy}'. "
            f"Choose from: {list(STRATEGIES)}"
        )

    return STRATEGIES[strategy](
        graph,
        budget,
        seed=seed
    )
