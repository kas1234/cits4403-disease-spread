"""
Basic SIR model that simulates the spread of an infection
through a contact network.

States:
0 = Susceptible
1 = Infected
2 = Recovered or Vaccinated
"""

import random
import networkx as nx
import numpy as np


S, I, R = 0, 1, 2


def run_sir(graph: nx.Graph, beta: float, gamma: float,
            vaccinated: set | None = None, seed: int | None = None,
            max_steps: int = 500) -> dict:
    """
    Run one SIR simulation on the given network.

    beta is the probability that an infected person infects
    a susceptible neighbour.

    gamma is the probability that an infected person recovers.

    Vaccinated nodes start in the recovered state.
    """

    rng = random.Random(seed)

    if vaccinated is None:
        vaccinated = set()

    # Start everyone as susceptible
    nodes = list(graph.nodes())
    state = {node: S for node in nodes}

    # Vaccinated people are already immune
    for node in vaccinated:
        state[node] = R

    # Choose one non-vaccinated person to start the infection
    susceptible_nodes = [
        node for node in nodes if state[node] == S
    ]

    # If everyone is vaccinated, there is no outbreak
    if not susceptible_nodes:
        return _empty_result(len(nodes))

    patient_zero = rng.choice(susceptible_nodes)
    state[patient_zero] = I

    S_t = []
    I_t = []
    R_t = []

    time = 0

    while True:

        # Count the number of susceptible, infected and recovered nodes
        counts = _tally(state)

        S_t.append(counts[S])
        I_t.append(counts[I])
        R_t.append(counts[R])

        # Stop when there are no infected people left
        # or when the maximum number of steps is reached
        if counts[I] == 0 or time >= max_steps:
            break

        # Make a copy so all changes happen at the same time
        new_state = dict(state)

        infected_nodes = [
            node for node, status in state.items()
            if status == I
        ]

        # Try to infect susceptible neighbours
        for node in infected_nodes:
            for neighbour in graph.neighbors(node):
                if state[neighbour] == S:
                    if rng.random() < beta:
                        new_state[neighbour] = I

        # Try to recover infected people
        for node in infected_nodes:
            if rng.random() < gamma:
                new_state[node] = R

        state = new_state
        time += 1

    # Find the highest number of infected people at one time
    peak_infected = max(I_t)

    return {
        "S_t": S_t,
        "I_t": I_t,
        "R_t": R_t,
        # Vaccinated people start in the R state, so remove them here:
        # final_size is the fraction of the population that got infected.
        "final_size": (R_t[-1] - len(vaccinated)) / len(nodes),
        "peak_infected": peak_infected,
        "time_to_peak": int(np.argmax(I_t)),
        "duration": len(I_t) - 1
    }


def _tally(state: dict) -> dict:
    """Count how many nodes are in each SIR state."""

    counts = {
        S: 0,
        I: 0,
        R: 0
    }

    for status in state.values():
        counts[status] += 1

    return counts


def _empty_result(n: int) -> dict:
    """Return the result when everyone is vaccinated."""

    return {
        "S_t": [n],
        "I_t": [0],
        "R_t": [0],
        "final_size": 0.0,
        "peak_infected": 0,
        "time_to_peak": 0,
        "duration": 0
    }
