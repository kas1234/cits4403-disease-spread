import csv
import os
import statistics

import networkx as nx


POPULATION = 100
AVERAGE_DEGREE = 4
RUNS = 100
BASE_SEED = 42

RESULT_FOLDER = "results"

CSV_PATH = os.path.join(
    RESULT_FOLDER,
    "network_properties.csv",
)


NETWORK_TYPES = [
    "random",
    "small_world",
    "scale_free",
]


def create_network(
    network_type,
    seed,
):
    if network_type == "random":

        connection_probability = (
            AVERAGE_DEGREE
            / (POPULATION - 1)
        )

        return nx.erdos_renyi_graph(
            n=POPULATION,
            p=connection_probability,
            seed=seed,
        )

    if network_type == "small_world":

        return nx.watts_strogatz_graph(
            n=POPULATION,
            k=AVERAGE_DEGREE,
            p=0.1,
            seed=seed,
        )

    if network_type == "scale_free":

        return nx.barabasi_albert_graph(
            n=POPULATION,
            m=2,
            seed=seed,
        )

    raise ValueError(
        f"Unknown network type: {network_type}"
    )


def calculate_properties(
    graph,
):
    degrees = [
        degree
        for _, degree
        in graph.degree()
    ]

    average_degree = (
        sum(degrees)
        / len(degrees)
    )

    clustering = (
        nx.average_clustering(
            graph
        )
    )

    maximum_degree = max(
        degrees
    )

    return (
        average_degree,
        clustering,
        maximum_degree,
    )


if __name__ == "__main__":

    os.makedirs(
        RESULT_FOLDER,
        exist_ok=True,
    )

    summary_results = []

    for network_type in NETWORK_TYPES:

        average_degrees = []
        clustering_values = []
        maximum_degrees = []

        for run in range(RUNS):

            seed = (
                BASE_SEED
                + run
            )

            graph = create_network(
                network_type,
                seed,
            )

            (
                average_degree,
                clustering,
                maximum_degree,
            ) = calculate_properties(
                graph
            )

            average_degrees.append(
                average_degree
            )

            clustering_values.append(
                clustering
            )

            maximum_degrees.append(
                maximum_degree
            )

        result = {
            "network": network_type,
            "mean_average_degree":
                statistics.mean(
                    average_degrees
                ),
            "std_average_degree":
                statistics.stdev(
                    average_degrees
                ),
            "mean_clustering":
                statistics.mean(
                    clustering_values
                ),
            "std_clustering":
                statistics.stdev(
                    clustering_values
                ),
            "mean_maximum_degree":
                statistics.mean(
                    maximum_degrees
                ),
        }

        summary_results.append(
            result
        )

        print()
        print(
            "Network:",
            network_type
        )

        print(
            "Average degree:",
            round(
                result[
                    "mean_average_degree"
                ],
                3,
            )
        )

        print(
            "Average clustering:",
            round(
                result[
                    "mean_clustering"
                ],
                3,
            )
        )

        print(
            "Average maximum degree:",
            round(
                result[
                    "mean_maximum_degree"
                ],
                3,
            )
        )

    with open(
        CSV_PATH,
        "w",
        newline="",
    ) as csv_file:

        fieldnames = [
            "network",
            "mean_average_degree",
            "std_average_degree",
            "mean_clustering",
            "std_clustering",
            "mean_maximum_degree",
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(
            summary_results
        )

    print()
    print(
        "Network property comparison completed."
    )

    print(
        "Results saved as:",
        CSV_PATH
    )