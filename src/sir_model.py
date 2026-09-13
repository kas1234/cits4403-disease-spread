"""
Core discrete-time SIR simulation over a static contact network.

States: 0 = Susceptible, 1 = Infected, 2 = Recovered (includes vaccinated).
"""

import random
import networkx as nx
import numpy as np

S, I, R = 0, 1, 2


def run_sir(graph: nx.Graph, beta: float, gamma: float,
            vaccinated: set | None = None, seed: int | None = None,
            max_steps: int = 500) -> dict:
    """
    Run one stochastic SIR simulation to completion (or until max_steps).

    Parameters
    ----------
    graph : the contact network
    beta  : per-timestep transmission probability, infected -> susceptible neighbour
    gamma : per-timestep recovery probability for an infected node
    vaccinated : set of node ids that start Recovered (immune)
    seed  : RNG seed for reproducibility
    max_steps : safety cap on simulation length

    Returns
    -------
    dict with:
      'S_t', 'I_t', 'R_t' : lists, counts per compartment at each timestep
      'final_size'        : fraction of the population ever infected
      'peak_infected'     : max number infected at once
      'time_to_peak'      : timestep at which infection peaked
      'duration'          : number of timesteps until I hit 0
    """
    rng = random.Random(seed)
    vaccinated = vaccinated or set()

    nodes = list(graph.nodes())
    state = {node: S for node in nodes}
    for node in vaccinated:
        state[node] = R

    # seed the outbreak with one random non-vaccinated node
    susceptible_nodes = [n for n in nodes if state[n] == S]
    if not susceptible_nodes:
        # everyone vaccinated -- no outbreak possible
        return _empty_result(len(nodes))
    patient_zero = rng.choice(susceptible_nodes)
    state[patient_zero] = I

    S_t, I_t, R_t = [], [], []
    t = 0
    while True:
        counts = _tally(state)
        S_t.append(counts[S])
        I_t.append(counts[I])
        R_t.append(counts[R])

        if counts[I] == 0 or t >= max_steps:
            break

        new_state = dict(state)
        infected_nodes = [n for n, s in state.items() if s == I]

        # transmission
        for node in infected_nodes:
            for neighbour in graph.neighbors(node):
                if state[neighbour] == S and rng.random() < beta:
                    new_state[neighbour] = I

        # recovery
        for node in infected_nodes:
            if rng.random() < gamma:
                new_state[node] = R

        state = new_state
        t += 1

    peak_infected = max(I_t)
    return {
        "S_t": S_t,
        "I_t": I_t,
        "R_t": R_t,
        "final_size": R_t[-1] / len(nodes),
        "peak_infected": peak_infected,
        "time_to_peak": int(np.argmax(I_t)),
        "duration": len(I_t) - 1,
    }


def _tally(state: dict) -> dict:
    counts = {S: 0, I: 0, R: 0}
    for v in state.values():
        counts[v] += 1
    return counts


def _empty_result(n: int) -> dict:
    return {
        "S_t": [n], "I_t": [0], "R_t": [0],
        "final_size": 0.0, "peak_infected": 0,
        "time_to_peak": 0, "duration": 0,
    }
