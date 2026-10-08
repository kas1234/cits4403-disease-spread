"""
Tests that the SIR simulation in src/sir_model.py follows its rules.

Each test uses a small graph where the correct answer can be worked out by
hand, including boundary cases (no transmission, certain transmission,
everyone vaccinated, disconnected network).
"""

import networkx as nx
import pytest

from src.sir_model import run_sir


def test_no_transmission_when_beta_is_zero():
    graph = nx.complete_graph(50)
    result = run_sir(graph, beta=0.0, gamma=0.5, seed=1)
    # only the first infected person ever gets the disease
    assert result["final_size"] == pytest.approx(1 / 50)
    assert result["peak_infected"] == 1


def test_certain_transmission_infects_everyone_in_connected_graph():
    graph = nx.complete_graph(20)
    result = run_sir(graph, beta=1.0, gamma=1.0, seed=1)
    assert result["final_size"] == pytest.approx(1.0)
    assert result["duration"] == 2  # step 1 infects everyone, step 2 everyone recovers


def test_no_one_recovers_while_gamma_is_zero_until_step_limit():
    graph = nx.path_graph(10)
    result = run_sir(graph, beta=1.0, gamma=0.0, seed=1, max_steps=30)
    # nobody ever recovers, so the run stops at the step limit with everyone infected
    assert result["I_t"][-1] == 10
    assert result["duration"] == 30


def test_everyone_vaccinated_means_no_outbreak():
    graph = nx.complete_graph(10)
    result = run_sir(graph, beta=1.0, gamma=0.5, vaccinated=set(graph.nodes()), seed=1)
    assert result["final_size"] == 0.0
    assert result["peak_infected"] == 0
    assert result["duration"] == 0


def test_vaccinated_people_are_never_counted_as_infected():
    graph = nx.complete_graph(100)
    vaccinated = set(range(30))
    result = run_sir(graph, beta=1.0, gamma=1.0, vaccinated=vaccinated, seed=3)
    # the other 70 people all get infected, the 30 vaccinated do not
    assert result["final_size"] == pytest.approx(0.70)


def test_vaccinating_the_hub_of_a_star_stops_the_spread():
    star = nx.star_graph(10)  # node 0 is the hub, nodes 1..10 are leaves
    result = run_sir(star, beta=1.0, gamma=1.0, vaccinated={0}, seed=5)
    # the first infected person is a leaf, and its only neighbour is immune
    assert result["final_size"] == pytest.approx(1 / 11)


def test_infection_does_not_cross_between_disconnected_components():
    graph = nx.disjoint_union(nx.complete_graph(10), nx.complete_graph(10))
    result = run_sir(graph, beta=1.0, gamma=1.0, seed=2)
    assert result["final_size"] == pytest.approx(0.5)


def test_population_is_conserved_at_every_step():
    graph = nx.erdos_renyi_graph(200, 0.03, seed=4)
    result = run_sir(graph, beta=0.2, gamma=0.1, vaccinated=set(range(20)), seed=4)
    for s, i, r in zip(result["S_t"], result["I_t"], result["R_t"]):
        assert s + i + r == 200


def test_same_seed_gives_identical_results_and_different_seed_can_differ():
    graph = nx.erdos_renyi_graph(100, 0.05, seed=1)
    a = run_sir(graph, beta=0.1, gamma=0.1, seed=7)
    b = run_sir(graph, beta=0.1, gamma=0.1, seed=7)
    assert a["I_t"] == b["I_t"]
    others = {tuple(run_sir(graph, beta=0.1, gamma=0.1, seed=s)["I_t"]) for s in range(8)}
    assert len(others) > 1


def test_outputs_are_consistent_with_each_other():
    graph = nx.erdos_renyi_graph(150, 0.04, seed=9)
    result = run_sir(graph, beta=0.15, gamma=0.1, seed=9)
    assert 0.0 <= result["final_size"] <= 1.0
    assert result["peak_infected"] == max(result["I_t"])
    assert result["I_t"][result["time_to_peak"]] == result["peak_infected"]
    assert result["duration"] == len(result["I_t"]) - 1
    assert result["I_t"][-1] == 0  # the run ended because nobody was left infected
