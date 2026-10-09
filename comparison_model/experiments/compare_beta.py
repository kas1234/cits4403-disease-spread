import csv
import os
from statistics import mean

import matplotlib.pyplot as plt

from compare_vaccination import (
    BASE_SEED,
    GRAPH_FOLDER,
    RUNS,
    run_simulation,
)


# --------------------------------------------------
# BETA VALUES TO TEST
# --------------------------------------------------

BETAS = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
]


# --------------------------------------------------
# NETWORK TYPES
# --------------------------------------------------

NETWORK_TYPES = [
    "random",
    "small_world",
    "scale_free",
]


# --------------------------------------------------
# VACCINATION STRATEGIES
# --------------------------------------------------

STRATEGIES = {
    "No Vaccination": (
        0.0,
        "none",
    ),
    "20% Random": (
        0.2,
        "random",
    ),
    "20% Targeted": (
        0.2,
        "targeted",
    ),
}


# --------------------------------------------------
# RESULT LOCATIONS
# --------------------------------------------------

RESULT_FOLDER = "results"

CSV_PATH = os.path.join(
    RESULT_FOLDER,
    "beta_sweep_results.csv",
)


# --------------------------------------------------
# RUN BETA EXPERIMENT
# --------------------------------------------------

if __name__ == "__main__":

    os.makedirs(
        GRAPH_FOLDER,
        exist_ok=True,
    )

    os.makedirs(
        RESULT_FOLDER,
        exist_ok=True,
    )

    raw_results = []
    summary_results = []

    # --------------------------------------------------
    # RUN ALL EXPERIMENTS
    # --------------------------------------------------

    for network_type in NETWORK_TYPES:

        print()
        print("=" * 60)
        print("NETWORK:", network_type)
        print("=" * 60)

        for (
            strategy_name,
            strategy_settings,
        ) in STRATEGIES.items():

            vaccination_rate = strategy_settings[0]
            strategy = strategy_settings[1]

            print()
            print("Strategy:", strategy_name)
            print("-" * 40)

            for beta in BETAS:

                condition_results = []

                for run in range(RUNS):

                    seed = BASE_SEED + run

                    (
                        peak,
                        epidemic,
                        time_to_peak,
                        duration,
                    ) = run_simulation(
                        vaccination_rate,
                        strategy,
                        network_type,
                        seed,
                        beta,
                    )

                    result = {
                        "network": network_type,
                        "strategy": strategy_name,
                        "beta": beta,
                        "run": run + 1,
                        "seed": seed,
                        "peak_infections": peak,
                        "epidemic_size": epidemic,
                        "time_to_peak": time_to_peak,
                        "duration": duration,
                    }

                    raw_results.append(result)
                    condition_results.append(result)

                average_peak = mean(
                    result["peak_infections"]
                    for result in condition_results
                )

                average_epidemic = mean(
                    result["epidemic_size"]
                    for result in condition_results
                )

                average_time_to_peak = mean(
                    result["time_to_peak"]
                    for result in condition_results
                )

                average_duration = mean(
                    result["duration"]
                    for result in condition_results
                )

                summary_results.append(
                    {
                        "network": network_type,
                        "strategy": strategy_name,
                        "beta": beta,
                        "peak_infections": average_peak,
                        "epidemic_size": average_epidemic,
                        "time_to_peak": average_time_to_peak,
                        "duration": average_duration,
                    }
                )

                print(f"Beta {beta:.2f}")

                print(
                    "  Peak infections:",
                    round(average_peak, 2),
                )

                print(
                    "  Epidemic size:",
                    round(average_epidemic, 2),
                )

                print(
                    "  Time to peak:",
                    round(average_time_to_peak, 2),
                )

                print(
                    "  Duration:",
                    round(average_duration, 2),
                )

    # --------------------------------------------------
    # SAVE INDIVIDUAL RUNS TO CSV
    # --------------------------------------------------

    with open(
        CSV_PATH,
        "w",
        newline="",
    ) as csv_file:

        fieldnames = [
            "network",
            "strategy",
            "beta",
            "run",
            "seed",
            "peak_infections",
            "epidemic_size",
            "time_to_peak",
            "duration",
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(raw_results)

    # --------------------------------------------------
    # EPIDEMIC SIZE VS BETA
    # --------------------------------------------------

    for network_type in NETWORK_TYPES:

        plt.figure(
            figsize=(9, 5)
        )

        for strategy_name in STRATEGIES:

            values = [
                result
                for result in summary_results
                if (
                    result["network"] == network_type
                    and result["strategy"] == strategy_name
                )
            ]

            x_values = [
                result["beta"]
                for result in values
            ]

            y_values = [
                result["epidemic_size"]
                for result in values
            ]

            plt.plot(
                x_values,
                y_values,
                marker="o",
                label=strategy_name,
            )

        plt.xlabel(
            "Transmission Probability (Beta)"
        )

        plt.ylabel(
            "Average Epidemic Size"
        )

        plt.title(
            "Beta vs Epidemic Size - "
            + network_type.replace(
                "_",
                " ",
            ).title()
        )

        plt.legend()
        plt.grid(alpha=0.3)

        graph_path = os.path.join(
            GRAPH_FOLDER,
            "beta_epidemic_size_"
            + network_type
            + ".png",
        )

        plt.savefig(
            graph_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

    # --------------------------------------------------
    # PEAK INFECTIONS VS BETA
    # --------------------------------------------------

    for network_type in NETWORK_TYPES:

        plt.figure(
            figsize=(9, 5)
        )

        for strategy_name in STRATEGIES:

            values = [
                result
                for result in summary_results
                if (
                    result["network"] == network_type
                    and result["strategy"] == strategy_name
                )
            ]

            x_values = [
                result["beta"]
                for result in values
            ]

            y_values = [
                result["peak_infections"]
                for result in values
            ]

            plt.plot(
                x_values,
                y_values,
                marker="o",
                label=strategy_name,
            )

        plt.xlabel(
            "Transmission Probability (Beta)"
        )

        plt.ylabel(
            "Average Peak Infections"
        )

        plt.title(
            "Beta vs Peak Infections - "
            + network_type.replace(
                "_",
                " ",
            ).title()
        )

        plt.legend()
        plt.grid(alpha=0.3)

        graph_path = os.path.join(
            GRAPH_FOLDER,
            "beta_peak_"
            + network_type
            + ".png",
        )

        plt.savefig(
            graph_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

    # --------------------------------------------------
    # FINISHED
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("Beta experiment completed successfully.")
    print()

    print(
        "Individual simulation runs saved:",
        len(raw_results),
    )

    print(
        "Results saved as:",
        CSV_PATH,
    )

    print(
        "Graphs saved in:",
        GRAPH_FOLDER,
    )