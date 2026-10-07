import os
import random

import matplotlib.pyplot as plt
import networkx as nx


POPULATION = 100
INFECTION_PROBABILITY = 0.2
RECOVERY_PROBABILITY = 0.1
VACCINATION_RATE = 0.2
TIME_STEPS = 30

GRAPH_FOLDER = "results/graphs"


def create_network():
    graph = nx.erdos_renyi_graph(
        n=POPULATION,
        p=0.05
    )

    return graph


def initialise_states(graph):
    states = {}

    for node in graph.nodes:
        states[node] = "S"

    return states


def vaccinate_population(states):
    new_states = states.copy()

    all_nodes = list(
        new_states.keys()
    )

    number_to_vaccinate = int(
        POPULATION * VACCINATION_RATE
    )

    vaccinated_nodes = random.sample(
        all_nodes,
        number_to_vaccinate
    )

    for node in vaccinated_nodes:
        new_states[node] = "V"

    return new_states


def infect_patient_zero(states):
    new_states = states.copy()

    susceptible_nodes = [
        node
        for node, state in new_states.items()
        if state == "S"
    ]

    patient_zero = random.choice(
        susceptible_nodes
    )

    new_states[patient_zero] = "I"

    return new_states


def spread_infection(graph, states):
    new_states = states.copy()

    for node in graph.nodes:

        if states[node] == "I":

            for neighbour in graph.neighbors(node):

                if states[neighbour] == "S":

                    if random.random() < INFECTION_PROBABILITY:
                        new_states[neighbour] = "I"

    return new_states


def recover_infected(states):
    new_states = states.copy()

    for node, state in states.items():

        if state == "I":

            if random.random() < RECOVERY_PROBABILITY:
                new_states[node] = "R"

    return new_states


if __name__ == "__main__":

    os.makedirs(
        GRAPH_FOLDER,
        exist_ok=True
    )

    graph = create_network()

    states = initialise_states(
        graph
    )

    states = vaccinate_population(
        states
    )

    states = infect_patient_zero(
        states
    )

    print(
        "Population:",
        graph.number_of_nodes()
    )

    print(
        "Connections:",
        graph.number_of_edges()
    )

    initial_susceptible = sum(
        1 for state in states.values()
        if state == "S"
    )

    initial_infected = sum(
        1 for state in states.values()
        if state == "I"
    )

    initial_recovered = sum(
        1 for state in states.values()
        if state == "R"
    )

    initial_vaccinated = sum(
        1 for state in states.values()
        if state == "V"
    )

    susceptible_history = [
        initial_susceptible
    ]

    infected_history = [
        initial_infected
    ]

    recovered_history = [
        initial_recovered
    ]

    vaccinated_history = [
        initial_vaccinated
    ]

    print(
        f"Step 0: "
        f"S={initial_susceptible}, "
        f"I={initial_infected}, "
        f"R={initial_recovered}, "
        f"V={initial_vaccinated}"
    )

    for step in range(
        1,
        TIME_STEPS + 1
    ):

        states = spread_infection(
            graph,
            states
        )

        states = recover_infected(
            states
        )

        susceptible = sum(
            1 for state in states.values()
            if state == "S"
        )

        infected = sum(
            1 for state in states.values()
            if state == "I"
        )

        recovered = sum(
            1 for state in states.values()
            if state == "R"
        )

        vaccinated = sum(
            1 for state in states.values()
            if state == "V"
        )

        susceptible_history.append(
            susceptible
        )

        infected_history.append(
            infected
        )

        recovered_history.append(
            recovered
        )

        vaccinated_history.append(
            vaccinated
        )

        print(
            f"Step {step}: "
            f"S={susceptible}, "
            f"I={infected}, "
            f"R={recovered}, "
            f"V={vaccinated}"
        )

        if infected == 0:
            print("Outbreak ended.")
            break

    time_steps = range(
        len(infected_history)
    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        time_steps,
        susceptible_history,
        label="Susceptible"
    )

    plt.plot(
        time_steps,
        infected_history,
        label="Infected"
    )

    plt.plot(
        time_steps,
        recovered_history,
        label="Recovered"
    )

    plt.plot(
        time_steps,
        vaccinated_history,
        label="Vaccinated"
    )

    plt.xlabel(
        "Time Step"
    )

    plt.ylabel(
        "Number of People"
    )

    plt.title(
        "Disease Spread - SIRV Model"
    )

    plt.legend()

    plt.grid()

    graph_path = os.path.join(
        GRAPH_FOLDER,
        "sirv_model_graph.png"
    )

    plt.savefig(
        graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        "Graph saved as:",
        graph_path
    )

    peak_infections = max(
        infected_history
    )

    final_susceptible = (
        susceptible_history[-1]
    )

    final_vaccinated = (
        vaccinated_history[-1]
    )

    epidemic_size = (
        POPULATION
        - final_susceptible
        - final_vaccinated
    )

    print(
        "Peak infections:",
        peak_infections
    )

    print(
        "Total epidemic size:",
        epidemic_size
    )

    print(
        "Vaccinated population:",
        initial_vaccinated
    )