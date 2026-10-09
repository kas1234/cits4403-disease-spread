# Disease Spread Model — Network Structure vs Vaccination Strategy

For this project we're modelling how a disease spreads through a
population, but instead of assuming anyone can catch it from anyone else,
people are connected through a network — like a real contact network would
be. The idea is to see whether the shape of that network changes which
vaccination strategy actually works best.

**Research question:** if we can only vaccinate a limited number of people,
does it matter whether we pick randomly, target the most-connected people,
or target the people who connect different groups together? And does
the answer change depending on what the network looks like — random
connections, tight-knit communities, or a few super-connected hubs?

## What's in here

- `demo.py` — builds one network and runs a single outbreak
- `src/networks.py` — builds the different network types (random, small-world, scale-free)
- `src/vaccination.py` — the different vaccination strategies
- `src/sir_model.py` — the actual spread simulation (Susceptible → Infected → Recovered)
- `src/experiment.py` — runs the full sweep (topology x strategy x transmission rate, 30 replications each)
- `run_experiment.py` — entry point for the sweep; saves `results/sweep_results.csv` and phase-diagram plots
- `calibrate.py` — calibrates the model against a real outbreak; saves `results/calibration_search.csv` and a comparison plot
- `src/visualize.py` — makes the plots
- `notebooks/analysis.ipynb` — notebook that explains the model with its equations and turns `results/sweep_results.csv` into the summary tables and figures used in the report
- `utils/stats.py` — helper functions for means, confidence intervals and the "major outbreak" definition
- `data/` — the real outbreak numbers used for calibration (`boarding_school_1978.csv`) and where they come from
- `tests/` — automated tests that check the model rules, the vaccination strategies and the network builders
- `comparison_model/` — a second, independently written SIRV model (100 people, 20% vaccinated) used as a cross-check of the main model
- `report/` — the final report (`CITS4403_Report.pdf` and the Word version); the `.md` files are earlier drafts of individual sections

## Repository structure

```
cits4403-disease-spread/
+-- src/              model code: networks, vaccination strategies, SIR simulation, experiment runner
+-- utils/            helper functions (statistics)
+-- data/             real outbreak numbers used for calibration
+-- notebooks/        analysis notebook (model equations, tables, figures)
+-- tests/            automated tests (python -m pytest)
+-- results/          saved simulation output and figures
+-- report/           final report (PDF and Word) and early section drafts
+-- comparison_model/ second, independently written model used as a cross-check
+-- requirements.txt  dependencies
+-- README.md
```

## Our contribution

The SIR model, the three network types and targeted immunisation are well known; we do not claim
them as new. All of the code in this repository was written by us (no code was copied from other
projects), and the project's own contribution is the investigation built on top of them:

- a controlled comparison of four vaccination strategies (none, random, degree, betweenness) on
  three network types that are matched in size and average number of contacts, using the same random
  seeds for every strategy so that strategies are compared on identical networks;
- an analysis that separates how often an outbreak takes off from how large it is when it does,
  which shows that targeted vaccination on scale-free networks both prevents outbreaks and shrinks
  them, while on random networks it only shrinks them;
- a calibration against a real outbreak (1978 boarding-school influenza) that is honest about where
  the model fails (final size), including the correction of a misleadingly good fit caused by
  averaging runs that died out with runs that took off;
- the discovery and fix of a counting bug (vaccinated people counted as infected), now guarded by
  tests; and
- a second, independently written implementation (`comparison_model/`) used to cross-check the
  conclusions, with the differences between the two models discussed in the report.

## Assumptions we're making

- Each timestep, an infected person has a chance (`beta`) of infecting each
  susceptible neighbour, and a chance (`gamma`) of recovering.
- Vaccinated people are treated as already immune from the start — we're
  not modelling partial immunity or delayed rollout yet.
- The outbreak starts with one random person getting infected.
- The network stays fixed during a run — no new connections form mid-outbreak.

## Progress so far (Checkpoint 2)

- Ran the full sweep across all three network types, all four vaccination
  strategies, and seven transmission rates (30 stochastic replications per
  combination) — see `results/sweep_results.csv` and the phase-diagram plots.
- Headline finding: which vaccination strategy works best depends heavily
  on network structure. Results below are mean final size (fraction of the
  population infected) at beta = 0.10 with 10% of people vaccinated, over 30
  runs each:

  | Network | None | Random | Degree | Betweenness |
  |---|---|---|---|---|
  | Scale-free | 0.84 | 0.68 | **0.22** | 0.25 |
  | Small-world | 0.84 | 0.59 | 0.58 | **0.44** |
  | Random | 0.83 | 0.67 | 0.66 | 0.77 |

  On scale-free networks, targeting the most-connected people (degree) is by
  far the best, because a few hubs drive most of the spread. On small-world
  networks, targeting people with high betweenness (the ones bridging
  different clusters) works best. On plain random networks no node is
  structurally special, so targeting does not beat vaccinating at random
  (degree is about equal to random, betweenness is worse); at beta = 0.20
  random vaccination is the best option there.
- Calibrated the model against the 1978 English boarding-school flu outbreak
  (N=763, reported final size 0.671, peak of 298 around day 6). A complete-graph
  (homogeneous mixing) assumption spread far too fast to match any target, so we
  searched over contact networks (random and small-world) with different numbers
  of contacts, beta and gamma. On a network an outbreak often dies out at once,
  and averaging those runs with the major outbreaks gave a misleadingly good fit,
  so the calibration now scores only the runs where the outbreak took off
  (final size above 10%). The best fit is a random network with about 12
  contacts per person, beta 0.18 and gamma 0.5: the average peak (about 299) and
  its timing (day 8 against day 6) are close to the real outbreak, but the final
  size is far too high (0.97 against 0.67). A small-world network did not fit
  better. See `results/calibration_search.csv` and `calibration_comparison.png`.
- Added `notebooks/analysis.ipynb`, which reproduces every table and figure in the results
  section of the report, including confidence intervals and how often outbreaks
  take off.
- Added a second, independently written model in `comparison_model/` with its own
  beta sweep and graphs. It agrees that targeting the most-connected people beats
  random vaccination on scale-free networks.

## Issues encountered

- We found and fixed a counting bug: `final_size` treated vaccinated people
  (who start in the recovered state) as infected, which made every vaccination
  result 0.10 too high. After the fix and a re-run with 30 repeats the ordering
  of strategies is unchanged but the benefit of vaccination is larger than first
  reported (see Pull Request #4).
- The calibration still does not reproduce the final size of the real outbreak.
  Once an outbreak takes off on a network with enough contacts to spread this
  fast, it reaches almost everyone, while only two thirds of the boys were ill.
  Possible reasons (not yet tested) are that some boys were already immune and
  that a boarding school has dormitory and class structure that our simple
  networks do not have.
- Results are noisy: many runs die out immediately, so only differences larger
  than about 0.1 in final size should be trusted with 30 repetitions.

## What's next

- The final report is in `report/` (`CITS4403_Report.pdf`).
- Possible extensions: partial vaccine effectiveness, several vaccination
  coverages, networks that change during the outbreak, and calibration that
  allows part of the population to start immune.

## How to run

1. Install Python 3.10 or newer.
2. Install the libraries: `pip install -r requirements.txt`
3. Run one example outbreak: `python demo.py`
4. Run the full experiment (several minutes, saves CSVs and plots to `results/`): `python run_experiment.py`
5. Run the calibration against the 1978 boarding school outbreak: `python calibrate.py`
6. Run the tests: `python -m pytest`
7. Open the analysis notebook: `jupyter notebook notebooks/analysis.ipynb` (run it from the project root)
8. The comparison model has its own instructions in `comparison_model/`.
