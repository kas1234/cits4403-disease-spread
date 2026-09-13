"""
Quick single-run demo: build one network, run one SIR simulation, plot the
epidemic curve. Run this first to confirm the model mechanics work before
touching the full experiment sweep.
"""

from src.networks import build_network
from src.vaccination import get_vaccinated_set
from src.sir_model import run_sir
from src.visualize import plot_epidemic_curve

if __name__ == "__main__":
    N = 300
    AVG_DEGREE = 6
    BETA = 0.08       # transmission probability per contact per timestep
    GAMMA = 0.1        # recovery probability per timestep
    STRATEGY = "degree"
    BUDGET = 0.1       # vaccinate 10% of the population
    SEED = 42

    graph = build_network("scale_free", N, AVG_DEGREE, seed=SEED)
    vaccinated = get_vaccinated_set(STRATEGY, graph, BUDGET, seed=SEED)

    result = run_sir(graph, beta=BETA, gamma=GAMMA, vaccinated=vaccinated, seed=SEED)

    print(f"Final outbreak size: {result['final_size']:.1%} of population")
    print(f"Peak infected: {result['peak_infected']}")
    print(f"Time to peak: {result['time_to_peak']}")
    print(f"Outbreak duration: {result['duration']} timesteps")

    plot_epidemic_curve(
        result,
        title=f"SIR on scale-free network ({STRATEGY} vaccination, beta={BETA})",
        save_path="results/demo_epidemic_curve.png",
    )
    print("\nSaved plot to results/demo_epidemic_curve.png")
