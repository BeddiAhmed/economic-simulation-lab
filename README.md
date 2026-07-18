# Economic Simulation Lab

A small, reproducible agent-based computational economics project.

## Research question

How does a temporary demand shock affect unemployment, wages, prices, firm survival,
household consumption, and inequality under alternative behavioural assumptions?

This repository intentionally begins with a small model rather than an attempted
"digital twin." The goal is to establish a transparent scientific workflow that can
later absorb real microdata, richer institutions, and AI-based decision modules.

## Version 0.1 model

Agents:
- Households: work, earn wages, consume, save, and search for jobs.
- Firms: hire workers, set wages and prices, produce, sell, and update decisions.
- Government/policy environment: can introduce a household transfer.

Markets:
- Labour market
- Single consumption-goods market

Core outputs:
- Unemployment rate
- Mean wage
- Price level
- Inventory/output proxy
- Household consumption
- Wealth inequality
- Firm exits

## Setup

Requires Python 3.11 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

On Windows, activate with:

```powershell
.venv\Scripts\activate
```

Run one simulation:

```bash
python -m econlab.run --steps 120 --households 500 --firms 30 --seed 42
```

Run tests:

```bash
pytest
```

Outputs are written to `outputs/`.

## Recommended first experiment

Compare three scenarios over 100 random seeds:

1. Baseline
2. Negative demand shock in months 25–36
3. Same shock plus targeted household transfers

Primary estimands:
- Peak unemployment
- Cumulative output loss
- Consumption loss by wealth quintile
- Time to recovery

## Roadmap

- v0.1: transparent toy economy
- v0.2: explicit demand shock and batch experiments
- v0.3: empirical initialization from Canadian public data
- v0.4: multiple industries and input-output linkages
- v0.5: banking, credit, defaults, and monetary policy
- v0.6: selected AI decision modules benchmarked against rule-based agents

## Guardrail

Do not initially let large language models control every decision. Use them later for
specific behaviours where qualitative reasoning matters, and benchmark them against
simpler rules. Economic accounting, constraints, market institutions, and reproducible
randomness should remain deterministic code.
