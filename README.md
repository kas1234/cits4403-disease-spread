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
- `src/experiment.py` — runs the full sweep (topology x strategy x transmission rate, 15 replications each)
- `run_experiment.py` — entry point for the sweep; saves `results/sweep_results.csv` and phase-diagram plots
- `calibrate.py` — calibrates the model against a real outbreak; saves `results/calibration_search.csv` and a comparison plot
- `src/visualize.py` — makes the plots

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
  searched over average-degree contact networks instead. Best fit so far:
  avg_degree=12, beta=0.14, gamma=0.30, giving simulated final size 0.89 vs.
  target 0.67 and peak 335 vs. target 298 — in the right ballpark but not a
  tight match yet, see `results/calibration_search.csv` / `calibration_comparison.png`.

## Issues encountered

- We found and fixed a counting bug: `final_size` treated vaccinated people
  (who start in the recovered state) as infected, which made every vaccination
  result 0.10 too high. After the fix and a re-run with 30 repeats the ordering
  of strategies is unchanged but the benefit of vaccination is larger than first
  reported (see Pull Request #4).
- The calibration fit is still rough — the model tends to overshoot the
  real outbreak's final size and peak even at the best-scoring parameters.
  Worth investigating whether that's a network-structure issue (a random
  graph may not represent a boarding school's actual contact pattern well)
  or whether the error metric is weighting the three targets in a way that
  doesn't produce a great visual fit.

## What's next

- Tighten the calibration (try small-world or other structured networks for
  the boarding-school contact pattern instead of a purely random one).
- Write up the final report/checkpoint deliverable from these results.
