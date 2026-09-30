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
"""

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.networks import build_network
from src.sir_model import run_sir

N = 763
TARGET_FINAL_SIZE = 512 / 763
TARGET_PEAK = 298
TARGET_TIME_TO_PEAK = 6

N_REPS = 10
AVG_DEGREES = [5, 6, 7, 8, 10, 12]
BETAS = np.arange(0.06, 0.15, 0.01)
GAMMAS = np.arange(0.10, 0.35, 0.05)


def score(avg_degree, beta, gamma):
    finals, peaks, ttps = [], [], []
    for rep in range(N_REPS):
        graph = build_network("random", N, avg_degree, seed=rep)
        result = run_sir(graph, beta=beta, gamma=gamma, vaccinated=None, seed=rep)
        finals.append(result["final_size"])
        peaks.append(result["peak_infected"])
        ttps.append(result["time_to_peak"])
    return np.mean(finals), np.mean(peaks), np.mean(ttps)


if __name__ == "__main__":
    rows = []
    for avg_degree, beta, gamma in itertools.product(AVG_DEGREES, BETAS, GAMMAS):
        final, peak, ttp = score(avg_degree, beta, gamma)
        err = (
            ((final - TARGET_FINAL_SIZE) / TARGET_FINAL_SIZE) ** 2
            + ((peak - TARGET_PEAK) / TARGET_PEAK) ** 2
            + ((ttp - TARGET_TIME_TO_PEAK) / TARGET_TIME_TO_PEAK) ** 2
        )
        rows.append({"avg_degree": avg_degree, "beta": beta, "gamma": gamma,
                      "final_size": final, "peak_infected": peak,
                      "time_to_peak": ttp, "error": err})

    df = pd.DataFrame(rows)
    df.to_csv("results/calibration_search.csv", index=False)

    best = df.loc[df["error"].idxmin()]
    print("Best fit:")
    print(best)

    graph = build_network("random", N, int(best["avg_degree"]), seed=1)
    result = run_sir(graph, beta=best["beta"], gamma=best["gamma"], vaccinated=None, seed=1)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(result["I_t"],
            label=f"simulated (avg_degree={int(best['avg_degree'])}, beta={best['beta']:.2f}, gamma={best['gamma']:.2f})",
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
