from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from mesa import Model
from mesa.datacollection import DataCollector

from .agents import Firm, Household
from .metrics import gini


@dataclass(frozen=True)
class Shock:
    start: int = 25
    end: int = 36
    transfer: float = 0.0


class EconomyModel(Model):
    def __init__(
        self,
        n_households: int = 500,
        n_firms: int = 30,
        seed: int | None = None,
        shock: Shock | None = None,
    ) -> None:
        super().__init__(seed=seed)
        self.period = 0
        self.shock = shock or Shock()
        self.current_transfer = 0.0

        for _ in range(n_households):
            Household(
                self,
                skill=float(self.random.lognormvariate(0.0, 0.20)),
                wealth=max(0.0, self.random.lognormvariate(2.5, 0.80)),
                propensity_to_consume=min(
                    0.95, max(0.05, self.random.normalvariate(0.25, 0.06))
                ),
            )

        for _ in range(n_firms):
            Firm(
                self,
                productivity=max(1.0, self.random.normalvariate(8.0, 1.0)),
                initial_cash=max(50.0, self.random.normalvariate(250.0, 40.0)),
                wage_offer=max(1.0, self.random.normalvariate(5.0, 0.5)),
                price=max(0.5, self.random.normalvariate(2.0, 0.15)),
            )

        self._match_workers(initial=True)

        self.datacollector = DataCollector(
            model_reporters={
                "unemployment_rate": lambda m: m.unemployment_rate,
                "mean_wage": lambda m: m.mean_wage,
                "price_level": lambda m: m.price_level,
                "output_inventory": lambda m: m.total_inventory,
                "consumption": lambda m: m.total_consumption,
                "wealth_gini": lambda m: gini([h.wealth for h in m.households]),
                "active_firms": lambda m: sum(f.active for f in m.firms),
                "transfers": lambda m: m.current_transfer * len(m.households),
            }
        )
        self.datacollector.collect(self)

    @property
    def households(self) -> list[Household]:
        return list(self.agents_by_type[Household])

    @property
    def firms(self) -> list[Firm]:
        return list(self.agents_by_type[Firm])

    @property
    def unemployment_rate(self) -> float:
        households = self.households
        return sum(not h.employed for h in households) / len(households)

    @property
    def mean_wage(self) -> float:
        active = [f.wage_offer for f in self.firms if f.active]
        return float(np.mean(active)) if active else 0.0

    @property
    def price_level(self) -> float:
        active = [f.price for f in self.firms if f.active]
        return float(np.mean(active)) if active else 0.0

    @property
    def total_inventory(self) -> float:
        return sum(f.inventory for f in self.firms if f.active)

    @property
    def total_consumption(self) -> float:
        return sum(h.consumption for h in self.households)

    def _set_policy(self) -> None:
        self.current_transfer = (
            self.shock.transfer
            if self.shock.start <= self.period <= self.shock.end
            else 0.0
        )

    def _match_workers(self, initial: bool = False) -> None:
        unemployed = [h for h in self.households if not h.employed]
        self.random.shuffle(unemployed)

        firms = [f for f in self.firms if f.active]
        self.random.shuffle(firms)

        for firm in firms:
            if initial:
                target = max(1, len(self.households) // max(1, len(firms)))
            else:
                target = firm.desired_workers()

            vacancies = max(0, target - len(firm.workers))
            for _ in range(min(vacancies, len(unemployed))):
                worker = unemployed.pop()
                worker.employer = firm
                firm.workers.append(worker)

    def step(self) -> None:
        self.period += 1
        self._set_policy()

        self.agents_by_type[Household].do("reset_period")
        self.agents_by_type[Firm].do("reset_period")

        self._match_workers()
        self.agents_by_type[Firm].shuffle_do("produce_and_pay")
        self.agents_by_type[Household].shuffle_do("receive_income")
        self.agents_by_type[Household].shuffle_do("consume")
        self.agents_by_type[Firm].shuffle_do("close_books")

        self.datacollector.collect(self)
