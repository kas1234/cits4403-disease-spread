import os
import random

import matplotlib.pyplot as plt
import networkx as nx


# --------------------------------------------------
# MODEL SETTINGS
# --------------------------------------------------

POPULATION = 100

INFECTION_PROBABILITY = 0.2
RECOVERY_PROBABILITY = 0.1

TIME_STEPS = 200

# Increased from 30 to 100 for more reliable averages
RUNS = 100

AVERAGE_DEGREE = 4
BASE_SEED = 42

GRAPH_FOLDER = "results/graphs"


# --------------------------------------------------
# CREATE NETWORK
# --------------------------------------------------

def create_network(
    network_type,
    seed=None
):

    if network_type == "random":

        probability = (
            AVERAGE_DEGREE
            / (POPULATION - 1)
        )

        return nx.erdos_renyi_graph(
            n=POPULATION,
            p=probability,
            seed=seed
        )

    elif network_type == "small_world":

        return nx.watts_strogatz_graph(
            n=POPULATION,
            k=AVERAGE_DEGREE,
            p=0.1,
            seed=seed
        )

    elif network_type == "scale_free":

        return nx.barabasi_albert_graph(
            n=POPULATION,
            m=AVERAGE_DEGREE // 2,
            seed=seed
        )

    else:

        raise ValueError(
            "Unknown network type"
        )


# --------------------------------------------------
# INITIALISE STATES
# --------------------------------------------------

def initialise_states(graph):

    return {
        node: "S"
        for node in graph.nodes
    }


# --------------------------------------------------
# RANDOM VACCINATION
# --------------------------------------------------

def random_vaccination(
    states,
    vaccination_rate
):

    new_states = states.copy()

    number_to_vaccinate = int(
        POPULATION
        * vaccination_rate
    )

    if number_to_vaccinate == 0:

        return new_states

    vaccinated_nodes = random.sample(
        list(new_states.keys()),
        number_to_vaccinate
    )

    for node in vaccinated_nodes:

        new_states[node] = "V"

    return new_states


# --------------------------------------------------
# TARGETED VACCINATION
# --------------------------------------------------

def targeted_vaccination(
    graph,
    states,
    vaccination_rate
):

    new_states = states.copy()

    number_to_vaccinate = int(
        POPULATION
        * vaccination_rate
    )

    if number_to_vaccinate == 0:

        return new_states

    degree_list = sorted(
        graph.degree,
        key=lambda item: item[1],
        reverse=True
    )

    targeted_nodes = [
        node
        for node, degree
        in degree_list[
            :number_to_vaccinate
        ]
    ]

    for node in targeted_nodes:

        new_states[node] = "V"

    return new_states


# --------------------------------------------------
# INFECT PATIENT ZERO
# --------------------------------------------------

def infect_patient_zero(states):

    new_states = states.copy()

    susceptible_nodes = [
        node
        for node, state
        in new_states.items()
        if state == "S"
    ]

    if not susceptible_nodes:

        return new_states

    patient_zero = random.choice(
        susceptible_nodes
    )

    new_states[
        patient_zero
    ] = "I"

    return new_states


# --------------------------------------------------
# ONE SIMULATION STEP
# --------------------------------------------------

def simulation_step(
    graph,
    states,
    beta=INFECTION_PROBABILITY
):

    new_states = states.copy()

    infected_nodes = [
        node
        for node, state
        in states.items()
        if state == "I"
    ]

    # --------------------------------------------------
    # SPREAD INFECTION
    # --------------------------------------------------

    for node in infected_nodes:

        for neighbour in graph.neighbors(
            node
        ):

            if states[neighbour] == "S":

                if (
                    random.random()
                    < beta
                ):

                    new_states[
                        neighbour
                    ] = "I"

    # --------------------------------------------------
    # RECOVERY
    # --------------------------------------------------

    # Only people infected at the beginning of
    # this timestep can recover in this timestep.

    for node in infected_nodes:

        if (
            random.random()
            < RECOVERY_PROBABILITY
        ):

            new_states[
                node
            ] = "R"

    return new_states


# --------------------------------------------------
# RUN ONE SIMULATION
# --------------------------------------------------

def run_simulation(
    vaccination_rate,
    strategy,
    network_type,
    seed,
    beta=INFECTION_PROBABILITY
):

    # Make experiment reproducible
    random.seed(seed)

    # Create contact network
    graph = create_network(
        network_type,
        seed
    )

    # Everyone starts susceptible
    states = initialise_states(
        graph
    )

    # --------------------------------------------------
    # APPLY VACCINATION
    # --------------------------------------------------

    if strategy == "random":

        states = random_vaccination(
            states,
            vaccination_rate
        )

    elif strategy == "targeted":

        states = targeted_vaccination(
            graph,
            states,
            vaccination_rate
        )

    elif strategy == "none":

        pass

    else:

        raise ValueError(
            "Unknown vaccination strategy"
        )

    # --------------------------------------------------
    # START OUTBREAK
    # --------------------------------------------------

    states = infect_patient_zero(
        states
    )

    infected_history = [
        sum(
            1
            for state
            in states.values()
            if state == "I"
        )
    ]

    # --------------------------------------------------
    # RUN EPIDEMIC
    # --------------------------------------------------

    for _ in range(
        TIME_STEPS
    ):

        states = simulation_step(
            graph,
            states,
            beta
        )

        infected = sum(
            1
            for state
            in states.values()
            if state == "I"
        )

        infected_history.append(
            infected
        )

        # Stop once the epidemic finishes
        if infected == 0:

            break

    # --------------------------------------------------
    # CALCULATE RESULTS
    # --------------------------------------------------

    peak_infections = max(
        infected_history
    )

    time_to_peak = (
        infected_history.index(
            peak_infections
        )
    )

    epidemic_duration = (
        len(infected_history)
        - 1
    )

    final_susceptible = sum(
        1
        for state
        in states.values()
        if state == "S"
    )

    final_vaccinated = sum(
        1
        for state
        in states.values()
        if state == "V"
    )

    epidemic_size = (
        POPULATION
        - final_susceptible
        - final_vaccinated
    )

    return (
        peak_infections,
        epidemic_size,
        time_to_peak,
        epidemic_duration
    )


# --------------------------------------------------
# RUN REPEATED EXPERIMENT
# --------------------------------------------------

def run_experiment(
    vaccination_rate,
    strategy,
    network_type,
    beta=INFECTION_PROBABILITY
):

    peak_results = []
    epidemic_results = []
    time_to_peak_results = []
    duration_results = []

    for run in range(
        RUNS
    ):

        seed = (
            BASE_SEED
            + run
        )

        (
            peak,
            epidemic,
            time_to_peak,
            duration
        ) = run_simulation(
            vaccination_rate,
            strategy,
            network_type,
            seed,
            beta
        )

        peak_results.append(
            peak
        )

        epidemic_results.append(
            epidemic
        )

        time_to_peak_results.append(
            time_to_peak
        )

        duration_results.append(
            duration
        )

    # --------------------------------------------------
    # CALCULATE AVERAGES
    # --------------------------------------------------

    average_peak = (
        sum(peak_results)
        / len(peak_results)
    )

    average_epidemic = (
        sum(epidemic_results)
        / len(epidemic_results)
    )

    average_time_to_peak = (
        sum(time_to_peak_results)
        / len(time_to_peak_results)
    )

    average_duration = (
        sum(duration_results)
        / len(duration_results)
    )

    return (
        average_peak,
        average_epidemic,
        average_time_to_peak,
        average_duration
    )


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

if __name__ == "__main__":

    os.makedirs(
        GRAPH_FOLDER,
        exist_ok=True
    )

    network_types = [
        "random",
        "small_world",
        "scale_free"
    ]

    strategies = {

        "No Vaccination": (
            0.0,
            "none"
        ),

        "20% Random": (
            0.2,
            "random"
        ),

        "20% Targeted": (
            0.2,
            "targeted"
        )
    }

    results = {}


    # --------------------------------------------------
    # RUN ALL EXPERIMENTS
    # --------------------------------------------------

    for network_type in network_types:

        print()
        print(
            "=" * 50
        )

        print(
            "Network:",
            network_type
        )

        print(
            "=" * 50
        )

        results[
            network_type
        ] = {}

        for (
            strategy_name,
            strategy_settings
        ) in strategies.items():

            vaccination_rate = (
                strategy_settings[0]
            )

            strategy = (
                strategy_settings[1]
            )

            result = run_experiment(
                vaccination_rate,
                strategy,
                network_type
            )

            results[
                network_type
            ][
                strategy_name
            ] = result

            print()
            print(
                strategy_name
            )

            print(
                "Average peak infections:",
                round(
                    result[0],
                    2
                )
            )

            print(
                "Average epidemic size:",
                round(
                    result[1],
                    2
                )
            )

            print(
                "Average time to peak:",
                round(
                    result[2],
                    2
                )
            )

            print(
                "Average epidemic duration:",
                round(
                    result[3],
                    2
                )
            )


    # --------------------------------------------------
    # GRAPH SETTINGS
    # --------------------------------------------------

    network_labels = [
        "Random",
        "Small-World",
        "Scale-Free"
    ]

    strategy_names = list(
        strategies.keys()
    )

    x_positions = list(
        range(
            len(network_types)
        )
    )

    width = 0.25


    # --------------------------------------------------
    # PEAK INFECTION GRAPH
    # --------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    for index, strategy_name in enumerate(
        strategy_names
    ):

        peak_values = [
            results[
                network
            ][
                strategy_name
            ][0]

            for network
            in network_types
        ]

        positions = [
            x
            + (
                index - 1
            ) * width

            for x
            in x_positions
        ]

        plt.bar(
            positions,
            peak_values,
            width=width,
            label=strategy_name
        )

    plt.xticks(
        x_positions,
        network_labels
    )

    plt.xlabel(
        "Network Type"
    )

    plt.ylabel(
        "Average Peak Infections"
    )

    plt.title(
        "Peak Infections Across Network Types"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    peak_graph_path = os.path.join(
        GRAPH_FOLDER,
        "network_peak_comparison.png"
    )

    plt.savefig(
        peak_graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    # --------------------------------------------------
    # EPIDEMIC SIZE GRAPH
    # --------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    for index, strategy_name in enumerate(
        strategy_names
    ):

        epidemic_values = [
            results[
                network
            ][
                strategy_name
            ][1]

            for network
            in network_types
        ]

        positions = [
            x
            + (
                index - 1
            ) * width

            for x
            in x_positions
        ]

        plt.bar(
            positions,
            epidemic_values,
            width=width,
            label=strategy_name
        )

    plt.xticks(
        x_positions,
        network_labels
    )

    plt.xlabel(
        "Network Type"
    )

    plt.ylabel(
        "Average Epidemic Size"
    )

    plt.title(
        "Epidemic Size Across Network Types"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    epidemic_graph_path = os.path.join(
        GRAPH_FOLDER,
        "network_epidemic_size_comparison.png"
    )

    plt.savefig(
        epidemic_graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    # --------------------------------------------------
    # TIME TO PEAK GRAPH
    # --------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    for index, strategy_name in enumerate(
        strategy_names
    ):

        time_values = [
            results[
                network
            ][
                strategy_name
            ][2]

            for network
            in network_types
        ]

        positions = [
            x
            + (
                index - 1
            ) * width

            for x
            in x_positions
        ]

        plt.bar(
            positions,
            time_values,
            width=width,
            label=strategy_name
        )

    plt.xticks(
        x_positions,
        network_labels
    )

    plt.xlabel(
        "Network Type"
    )

    plt.ylabel(
        "Average Time to Peak"
    )

    plt.title(
        "Time to Peak Across Network Types"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    time_graph_path = os.path.join(
        GRAPH_FOLDER,
        "network_time_to_peak_comparison.png"
    )

    plt.savefig(
        time_graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    # --------------------------------------------------
    # EPIDEMIC DURATION GRAPH
    # --------------------------------------------------

    plt.figure(
        figsize=(10, 6)
    )

    for index, strategy_name in enumerate(
        strategy_names
    ):

        duration_values = [
            results[
                network
            ][
                strategy_name
            ][3]

            for network
            in network_types
        ]

        positions = [
            x
            + (
                index - 1
            ) * width

            for x
            in x_positions
        ]

        plt.bar(
            positions,
            duration_values,
            width=width,
            label=strategy_name
        )

    plt.xticks(
        x_positions,
        network_labels
    )

    plt.xlabel(
        "Network Type"
    )

    plt.ylabel(
        "Average Epidemic Duration"
    )

    plt.title(
        "Epidemic Duration Across Network Types"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    duration_graph_path = os.path.join(
        GRAPH_FOLDER,
        "network_duration_comparison.png"
    )

    plt.savefig(
        duration_graph_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


    # --------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------

    print()
    print(
        "=" * 50
    )

    print(
        "Experiments completed successfully."
    )

    print(
        "Number of runs per experiment:",
        RUNS
    )

    print()

    print(
        "Peak comparison graph saved as:",
        peak_graph_path
    )

    print(
        "Epidemic size graph saved as:",
        epidemic_graph_path
    )

    print(
        "Time to peak graph saved as:",
        time_graph_path
    )

    print(
        "Duration graph saved as:",
        duration_graph_path
    )