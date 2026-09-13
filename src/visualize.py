"""
Plotting helpers: single-run epidemic curves and sweep phase diagrams.
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_epidemic_curve(result: dict, title: str = "SIR epidemic curve",
                         save_path: str | None = None):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(result["S_t"], label="Susceptible")
    ax.plot(result["I_t"], label="Infected")
    ax.plot(result["R_t"], label="Recovered / Vaccinated")
    ax.set_xlabel("timestep")
    ax.set_ylabel("number of nodes")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig


def plot_phase_diagram(df: pd.DataFrame, metric: str = "final_size",
                        save_path: str | None = None):
    """
    One subplot per topology; within each, final outbreak size vs. beta,
    one line per vaccination strategy (mean over replications, with
    min/max shading to show variability across stochastic runs).
    """
    topologies = df["topology"].unique()
    fig, axes = plt.subplots(1, len(topologies), figsize=(5 * len(topologies), 4.5),
                              sharey=True)
    if len(topologies) == 1:
        axes = [axes]

    for ax, topology in zip(axes, topologies):
        sub = df[df["topology"] == topology]
        for strategy in sub["strategy"].unique():
            strat_df = sub[sub["strategy"] == strategy]
            grouped = strat_df.groupby("beta")[metric].agg(["mean", "min", "max"])
            ax.plot(grouped.index, grouped["mean"], label=strategy, marker="o")
            ax.fill_between(grouped.index, grouped["min"], grouped["max"], alpha=0.15)
        ax.set_title(topology)
        ax.set_xlabel("beta (transmission probability)")

    axes[0].set_ylabel(metric)
    axes[0].legend()
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150)
    return fig
