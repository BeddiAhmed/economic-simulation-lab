# Research Protocol

## Initial question

How do temporary income transfers alter the distribution and persistence of a demand
shock?

## Hypotheses

- H1: Transfers reduce peak unemployment.
- H2: Transfers reduce cumulative consumption loss.
- H3: Transfers shorten recovery time.
- H4: Transfers reduce short-run increases in wealth inequality.
- H5: Results depend on heterogeneous consumption propensities.

## Experimental design

For every scenario:

- Run at least 100 random seeds.
- Use identical seeds across scenarios.
- Store all parameter values and outputs.
- Report median, interquartile range, and 90% simulation intervals.
- Predefine outcome statistics before reviewing results.

## Validation ladder

1. Code verification: unit tests and accounting checks.
2. Face validity: inspect trajectories and agent histories.
3. Pattern validity: reproduce qualitative stylized facts.
4. Moment matching: compare selected simulated and empirical moments.
5. Out-of-sample validation: calibrate on one period, evaluate another.
6. Policy validation: reproduce a known historical intervention where possible.
