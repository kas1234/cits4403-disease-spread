# Network Structure vs. Vaccination Strategy — SIR Epidemic Model

**Research question:** How does contact-network structure interact with
vaccination strategy to determine epidemic outcomes, under a fixed
vaccination budget?

## Project structure

```
disease-spread-project/
├── src/
│   ├── networks.py       # network topology generators
│   ├── vaccination.py    # vaccination strategy implementations
│   ├── sir_model.py       # core SIR simulation over a graph
│   ├── experiment.py      # parameter sweep + multiple replications
│   └── visualize.py       # epidemic curves + phase diagrams
├── demo.py                 # quick single-run demo (start here)
├── run_experiment.py       # full parameter sweep (Checkpoint 2 target)
├── results/                # generated figures / csv output land here
└── requirements.txt
```

## Getting started

```bash
pip install -r requirements.txt
python demo.py              # single run: builds one network, runs SIR, plots the curve
python run_experiment.py    # full sweep across topologies x strategies x transmission prob
```

## Model assumptions (edit these as your group refines them)

- Discrete-time SIR: each infected node infects each susceptible neighbour
  independently with probability `beta` per timestep, and recovers with
  probability `gamma` per timestep (so infectious duration ~ Geometric(gamma)).
- A vaccinated node is treated as permanently Recovered (immune) from t=0 —
  i.e. vaccination removes it from the susceptible pool before the outbreak
  starts. This is a simplifying assumption worth discussing/relaxing later
  (e.g. partial efficacy, delayed rollout).
- The outbreak is seeded by infecting one randomly chosen non-vaccinated node.
- Network is static for the duration of one simulation run (no rewiring).

## Next steps for your group

1. Run `demo.py`, confirm the epidemic curve looks sensible (rises, peaks, decays).
2. Sanity-check against theory: sweep `beta` on an Erdos-Renyi graph and confirm
   there's a threshold below which outbreaks fizzle out and above which they
   take off (the epidemic threshold).
3. Run `run_experiment.py` and look at `results/phase_diagram.png` — this is
   your core Checkpoint 2 result.
4. Decide on your "twist" extension (behavioural feedback, superspreader
   clustering, spatial mobility — see conversation notes) once the baseline
   is solid.
