"""Tests for the network builders in src/networks.py."""

import networkx as nx
import pytest

from src.networks import build_network


@pytest.mark.parametrize("topology", ["random", "small_world", "scale_free"])
def test_network_has_requested_size_and_average_degree(topology):
    graph = build_network(topology, 300, 6, seed=1)
    average_degree = sum(d for _, d in graph.degree()) / graph.number_of_nodes()
    assert graph.number_of_nodes() == 300
    # all three types are built to have about six contacts per person
    assert average_degree == pytest.approx(6, abs=0.8)


def test_scale_free_network_has_hubs_and_random_network_does_not():
    scale_free = build_network("scale_free", 300, 6, seed=1)
    random_net = build_network("random", 300, 6, seed=1)
    assert max(d for _, d in scale_free.degree()) > max(d for _, d in random_net.degree())
    assert max(d for _, d in scale_free.degree()) >= 25


def test_small_world_network_is_clustered():
    small_world = build_network("small_world", 300, 6, seed=1)
    random_net = build_network("random", 300, 6, seed=1)
    assert nx.average_clustering(small_world) > 3 * nx.average_clustering(random_net)


def test_same_seed_gives_same_network():
    a = build_network("random", 100, 6, seed=3)
    b = build_network("random", 100, 6, seed=3)
    assert sorted(a.edges()) == sorted(b.edges())


def test_unknown_topology_raises_an_error():
    with pytest.raises(ValueError):
        build_network("lattice", 50, 4)
