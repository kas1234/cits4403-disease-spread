"""
Functions for creating graphs from the SIR simulation results.
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_epidemic_curve(result: dict,
                        title: str = "SIR epidemic curve",
                        save_path: str | None = None):
    """Plot the number of susceptible, infected and recovered nodes over time."""

    fig, ax = plt.subplots(figsize=(7, 4.5))

    # Plot each SIR group
    ax.plot(result["S_t"], label="Susceptible")
    ax.plot(result["I_t"], label="Infected")
    ax.plot(result["R_t"], label="Recovered / Vaccinated")

    ax.set_xlabel("Timestep")
    ax.set_ylabel("Number of nodes")
    ax.set_title(title)
    ax.legend()

    fig.tight_layout()

    # Save the graph if a file path was provided
    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig


def plot_phase_diagram(df: pd.DataFrame,
                       metric: str = "final_size",
                       save_path: str | None = None):
    """
    Compare different vaccination strategies for each network type.

    The graph shows the average result for each transmission probability.
    The shaded area shows the minimum and maximum results from the
    different simulation runs.
    """

    topologies = df["topology"].unique()

    # Create one graph for each network type
    fig, axes = plt.subplots(
        1,
        len(topologies),
        figsize=(5 * len(topologies), 4.5),
        sharey=True
    )

    # Make axes a list when there is only one topology
    if len(topologies) == 1:
        axes = [axes]

    for ax, topology in zip(axes, topologies):

        # Get the results for this particular network type
        topology_data = df[df["topology"] == topology]

        for strategy in topology_data["strategy"].unique():

            # Get results for the current vaccination strategy
            strategy_data = topology_data[
                topology_data["strategy"] == strategy
            ]

            # Calculate average, minimum and maximum values for each beta
            grouped = strategy_data.groupby("beta")[metric].agg(
                ["mean", "min", "max"]
            )

            # Plot the average result
            ax.plot(
                grouped.index,
                grouped["mean"],
                label=strategy,
                marker="o"
            )

            # Show the range of results using shading
            ax.fill_between(
                grouped.index,
                grouped["min"],
                grouped["max"],
                alpha=0.15
            )

        ax.set_title(topology)
        ax.set_xlabel("Beta (transmission probability)")

    axes[0].set_ylabel(metric)
    axes[0].legend()

    fig.tight_layout()

    # Save the figure if a path was provided
    if save_path:
        fig.savefig(save_path, dpi=150)

    return fig
