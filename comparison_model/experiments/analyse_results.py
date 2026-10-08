import os
import pandas as pd


RESULTS_FILE = "results/beta_sweep_results.csv"
OUTPUT_FOLDER = "results/analysis"


def load_results():
    """Load simulation results from the beta sweep."""

    df = pd.read_csv(RESULTS_FILE)

    print("Results loaded successfully.")
    print("Number of simulation runs:", len(df))

    return df


def create_summary(df):
    """Calculate average results for each experimental condition."""

    summary = (
        df.groupby(
            [
                "network",
                "strategy",
                "beta"
            ]
        )
        .agg(
            mean_epidemic_size=(
                "epidemic_size",
                "mean"
            ),
            std_epidemic_size=(
                "epidemic_size",
                "std"
            ),
            mean_peak_infections=(
                "peak_infections",
                "mean"
            ),
            std_peak_infections=(
                "peak_infections",
                "std"
            ),
            mean_time_to_peak=(
                "time_to_peak",
                "mean"
            ),
            mean_duration=(
                "duration",
                "mean"
            )
        )
        .reset_index()
    )

    return summary


def compare_vaccination_strategies(df):
    """Compare vaccination strategies across all simulations."""

    comparison = (
        df.groupby("strategy")
        .agg(
            mean_epidemic_size=(
                "epidemic_size",
                "mean"
            ),
            mean_peak_infections=(
                "peak_infections",
                "mean"
            ),
            mean_time_to_peak=(
                "time_to_peak",
                "mean"
            ),
            mean_duration=(
                "duration",
                "mean"
            )
        )
        .reset_index()
    )

    return comparison


def compare_networks(df):
    """Compare epidemic behaviour across network structures."""

    comparison = (
        df.groupby("network")
        .agg(
            mean_epidemic_size=(
                "epidemic_size",
                "mean"
            ),
            mean_peak_infections=(
                "peak_infections",
                "mean"
            ),
            mean_time_to_peak=(
                "time_to_peak",
                "mean"
            ),
            mean_duration=(
                "duration",
                "mean"
            )
        )
        .reset_index()
    )

    return comparison


if __name__ == "__main__":

    os.makedirs(
        OUTPUT_FOLDER,
        exist_ok=True
    )

    results = load_results()

    summary = create_summary(
        results
    )

    strategy_comparison = (
        compare_vaccination_strategies(
            results
        )
    )

    network_comparison = (
        compare_networks(
            results
        )
    )

    print("\n--- Vaccination Strategy Comparison ---")
    print(
        strategy_comparison.to_string(
            index=False
        )
    )

    print("\n--- Network Comparison ---")
    print(
        network_comparison.to_string(
            index=False
        )
    )

    summary.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "experiment_summary.csv"
        ),
        index=False
    )

    strategy_comparison.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "vaccination_strategy_summary.csv"
        ),
        index=False
    )

    network_comparison.to_csv(
        os.path.join(
            OUTPUT_FOLDER,
            "network_summary.csv"
        ),
        index=False
    )

    print(
        "\nAnalysis files saved in:",
        OUTPUT_FOLDER
    )