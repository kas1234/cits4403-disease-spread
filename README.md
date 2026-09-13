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
- `src/visualize.py` — makes the plots

## Assumptions we're making

- Each timestep, an infected person has a chance (`beta`) of infecting each
  susceptible neighbour, and a chance (`gamma`) of recovering.
- Vaccinated people are treated as already immune from the start — we're
  not modelling partial immunity or delayed rollout yet.
- The outbreak starts with one random person getting infected.
- The network stays fixed during a run — no new connections form mid-outbreak.

## What's next

- Actually run this across a bunch of different transmission rates and see
  where it takes off vs. dies out.
- Compare all three network types against all three vaccination strategies.
- Validate the model against a real historical outbreak — planning to use
  the 1978 English boarding school flu outbreak (a well-documented,
  closed-population case with known outcomes) as a benchmark.
