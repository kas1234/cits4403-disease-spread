"""Tests for the vaccination strategies in src/vaccination.py."""

import networkx as nx
import pytest

from src.vaccination import get_vaccinated_set


@pytest.mark.parametrize("strategy", ["random", "degree", "betweenness"])
@pytest.mark.parametrize("budget", [0.0, 0.1, 0.25, 1.0])
def test_number_vaccinated_matches_budget(strategy, budget):
    graph = nx.erdos_renyi_graph(100, 0.06, seed=1)
    chosen = get_vaccinated_set(strategy, graph, budget, seed=1)
    assert len(chosen) == round(budget * 100)
    assert chosen <= set(graph.nodes())


def test_none_strategy_vaccinates_nobody():
    graph = nx.path_graph(20)
    assert get_vaccinated_set("none", graph, 0.5) == set()


def test_degree_strategy_picks_the_hub():
    star = nx.star_graph(10)  # node 0 has degree 10, all others degree 1
    assert get_vaccinated_set("degree", star, budget=1 / 11) == {0}


def test_betweenness_strategy_picks_the_bridge_between_two_clusters():
    # two cliques of 6 joined by a single bridge node 12
    graph = nx.disjoint_union(nx.complete_graph(6), nx.complete_graph(6))
    graph.add_edges_from([(12, 0), (12, 6)])
    assert get_vaccinated_set("betweenness", graph, budget=1 / 13) == {12}


def test_degree_strategy_chooses_highest_degrees():
    graph = nx.barabasi_albert_graph(200, 3, seed=2)
    chosen = get_vaccinated_set("degree", graph, 0.1)
    lowest_chosen = min(graph.degree(n) for n in chosen)
    highest_other = max(graph.degree(n) for n in graph.nodes() if n not in chosen)
    assert lowest_chosen >= highest_other


def test_random_strategy_is_reproducible_with_a_seed():
    graph = nx.path_graph(100)
    a = get_vaccinated_set("random", graph, 0.2, seed=5)
    b = get_vaccinated_set("random", graph, 0.2, seed=5)
    c = get_vaccinated_set("random", graph, 0.2, seed=6)
    assert a == b
    assert a != c


def test_unknown_strategy_raises_an_error():
    with pytest.raises(ValueError):
        get_vaccinated_set("telepathy", nx.path_graph(5), 0.2)
