"""
Calibrate the SIR model against a real, well-documented outbreak: the 1978
English boarding-school influenza outbreak.

Source: Anonymous (1978), "Influenza in a boarding school", British Medical
Journal 1:587. Widely cited summary statistics for this closed-population
outbreak:
  - N = 763 boys
  - 512 were confined to bed at some point over the outbreak
    (final size = 512 / 763 = 0.671)
  - peak of 298 in bed at once, around day 6
  - the outbreak lasted about 14 days

First attempt: modelled the school as a complete graph (everyone can
contact everyone), the classic "homogeneous mixing" assumption. That
turned out to spread far too fast and too completely to match the real
numbers at any beta/gamma -- with 762 neighbours per person, even a low
per-contact transmission probability infects almost everyone almost
immediately. So instead we search over a moderate average-degree contact
network (representing realistic daily contacts: classmates, dorm-mates,
meals) together with beta and gamma, and look for the combination whose
simulated outbreak best matches the three reported summary numbers.

Second attempt: on a network, a run either dies out almost immediately
(the first person recovers before infecting anyone) or becomes a major
outbreak. Averaging the two kinds of run together gave a misleadingly good
"fit" (the average of 0% and 99% can look like 67%). The real school outbreak
did take off, so we now score only the runs that became major outbreaks
(final size above 10%), report how often that happened, and also try a
small-world contact network as well as a random one. The search uses the
corrected final_size (vaccinated people are no longer counted as infected).
"""

import itertools
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.networks import build_network
from src.sir_model import run_sir

# Summary numbers of the real outbreak (see data/README.md for the source)
DATA_FILE = Path(__file__).parent / "data" / "boarding_school_1978.csv"
_real = pd.read_csv(DATA_FILE).set_index("quantity")["value"]
N = int(_real["population"])
TARGET_FINAL_SIZE = _real["confined_to_bed"] / _real["population"]
TARGET_PEAK = int(_real["peak_in_bed"])
TARGET_TIME_TO_PEAK = int(_real["day_of_peak"])

N_REPS = 10
TOPOLOGIES = ["random", "small_world"]
MAJOR_OUTBREAK = 0.10  # runs with a smaller final size count as "died out"
AVG_DEGREES = [6, 8, 10, 12]
BETAS = np.round(np.arange(0.04, 0.22, 0.02), 2)
GAMMAS = [0.20, 0.30, 0.40, 0.50]


def score(topology, avg_degree, beta, gamma):
    """Mean outcome over the runs that became major outbreaks."""
    finals, peaks, ttps = [], [], []
    for rep in range(N_REPS):
        graph = build_network(topology, N, avg_degree, seed=rep)
        result = run_sir(graph, beta=beta, gamma=gamma, vaccinated=None, seed=rep)
        if result["final_size"] > MAJOR_OUTBREAK:
            finals.append(result["final_size"])
            peaks.append(result["peak_infected"])
            ttps.append(result["time_to_peak"])
    takeoff = len(finals) / N_REPS
    if len(finals) < N_REPS / 2:
        return None  # outbreak usually dies out, so this setting cannot be calibrated
    return np.mean(finals), np.mean(peaks), np.mean(ttps), takeoff


if __name__ == "__main__":
    rows = []
    for topology, avg_degree, beta, gamma in itertools.product(TOPOLOGIES, AVG_DEGREES, BETAS, GAMMAS):
        scored = score(topology, avg_degree, beta, gamma)
        if scored is None:
            continue
        final, peak, ttp, takeoff = scored
        err = (
            ((final - TARGET_FINAL_SIZE) / TARGET_FINAL_SIZE) ** 2
            + ((peak - TARGET_PEAK) / TARGET_PEAK) ** 2
            + ((ttp - TARGET_TIME_TO_PEAK) / TARGET_TIME_TO_PEAK) ** 2
        )
        rows.append({"topology": topology, "avg_degree": avg_degree, "beta": beta, "gamma": gamma,
                      "final_size": final, "peak_infected": peak,
                      "time_to_peak": ttp, "takeoff_fraction": takeoff,
                      "error": err})

    df = pd.DataFrame(rows)
    df.to_csv("results/calibration_search.csv", index=False)

    best = df.loc[df["error"].idxmin()]
    print("Best fit:")
    print(best)
    print(f"Mean over major-outbreak runs only; {best['takeoff_fraction']:.0%} of runs took off.")

    # Plot the first run (seed 0, 1, 2, ...) that became a major outbreak.
    for seed in range(N_REPS):
        graph = build_network(best["topology"], N, int(best["avg_degree"]), seed=seed)
        result = run_sir(graph, beta=best["beta"], gamma=best["gamma"], vaccinated=None, seed=seed)
        if result["final_size"] > MAJOR_OUTBREAK:
            break

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(result["I_t"],
            label=f"simulated ({best['topology']}, avg_degree={int(best['avg_degree'])}, beta={best['beta']:.2f}, gamma={best['gamma']:.2f})",
            linewidth=2)
    ax.axhline(TARGET_PEAK, color="grey", linestyle="--", label=f"reported peak ({TARGET_PEAK})")
    ax.axvline(TARGET_TIME_TO_PEAK, color="grey", linestyle=":", label=f"reported time to peak (day {TARGET_TIME_TO_PEAK})")
    ax.set_xlabel("Day")
    ax.set_ylabel("Number infected")
    ax.set_title("Calibration against the 1978 English boarding-school flu outbreak")
    ax.legend()
    fig.tight_layout()
    fig.savefig("results/calibration_comparison.png", dpi=150)

    print(f"Simulated final size: {result['final_size']:.3f} (target {TARGET_FINAL_SIZE:.3f})")
    print(f"Simulated peak infected: {result['peak_infected']} (target {TARGET_PEAK})")
    print(f"Simulated time to peak: {result['time_to_peak']} (target {TARGET_TIME_TO_PEAK})")
    print("Saved results/calibration_search.csv and results/calibration_comparison.png")
