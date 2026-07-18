from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from .model import EconomyModel, Shock


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the Economic Simulation Lab model.")
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--households", type=int, default=500)
    parser.add_argument("--firms", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--shock-start", type=int, default=25)
    parser.add_argument("--shock-end", type=int, default=36)
    parser.add_argument("--transfer", type=float, default=0.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    model = EconomyModel(
        n_households=args.households,
        n_firms=args.firms,
        seed=args.seed,
        shock=Shock(args.shock_start, args.shock_end, args.transfer),
    )

    for _ in range(args.steps):
        model.step()

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    frame = model.datacollector.get_model_vars_dataframe()
    frame.index.name = "period"
    frame.to_csv(output_dir / f"run_seed_{args.seed}.csv")

    for column in ["unemployment_rate", "consumption", "price_level", "wealth_gini"]:
        ax = frame[column].plot(title=column.replace("_", " ").title())
        ax.set_xlabel("Period")
        ax.figure.tight_layout()
        ax.figure.savefig(output_dir / f"{column}_seed_{args.seed}.png", dpi=150)
        plt.close(ax.figure)

    print(frame.tail().to_string())
    print(f"\nSaved results to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
