from __future__ import annotations

from mesa import Agent


class Household(Agent):
    def __init__(
        self,
        model,
        skill: float,
        wealth: float,
        propensity_to_consume: float,
    ) -> None:
        super().__init__(model)
        self.skill = skill
        self.wealth = wealth
        self.propensity_to_consume = propensity_to_consume
        self.employer: Firm | None = None
        self.wage_income = 0.0
        self.transfer_income = 0.0
        self.consumption = 0.0

    @property
    def employed(self) -> bool:
        return self.employer is not None

    def reset_period(self) -> None:
        self.wage_income = 0.0
        self.transfer_income = 0.0
        self.consumption = 0.0

    def receive_income(self) -> None:
        if self.employer is not None:
            self.wage_income = self.employer.wage_offer * self.skill
            self.wealth += self.wage_income
        self.transfer_income = self.model.current_transfer
        self.wealth += self.transfer_income

    def consume(self) -> None:
        desired_budget = self.propensity_to_consume * max(self.wealth, 0.0)
        actual_budget = min(desired_budget, self.wealth)
        if actual_budget <= 0:
            return

        firms = [f for f in self.model.firms if f.inventory > 0 and f.active]
        if not firms:
            return

        firm = min(firms, key=lambda candidate: candidate.price)
        quantity = min(actual_budget / firm.price, firm.inventory)
        spending = quantity * firm.price

        firm.inventory -= quantity
        firm.revenue += spending
        self.wealth -= spending
        self.consumption += spending


class Firm(Agent):
    def __init__(
        self,
        model,
        productivity: float,
        initial_cash: float,
        wage_offer: float,
        price: float,
    ) -> None:
        super().__init__(model)
        self.productivity = productivity
        self.cash = initial_cash
        self.wage_offer = wage_offer
        self.price = price
        self.inventory = 0.0
        self.revenue = 0.0
        self.last_sales = 1.0
        self.workers: list[Household] = []
        self.active = True

    def reset_period(self) -> None:
        self.revenue = 0.0

    def desired_workers(self) -> int:
        if not self.active:
            return 0
        desired_output = max(self.last_sales, 1.0) * 1.05
        return max(1, int(round(desired_output / self.productivity)))

    def produce_and_pay(self) -> None:
        if not self.active:
            return

        wage_bill = sum(self.wage_offer * worker.skill for worker in self.workers)
        affordable_share = min(1.0, self.cash / wage_bill) if wage_bill > 0 else 1.0
        output = self.productivity * len(self.workers) * affordable_share

        self.inventory += output
        self.cash -= wage_bill * affordable_share

        if affordable_share < 1.0:
            self.fire_all()

    def close_books(self) -> None:
        if not self.active:
            return

        units_sold = self.revenue / max(self.price, 1e-9)
        stock_available = self.inventory + units_sold
        sales_rate = units_sold / max(stock_available, 1e-9)

        self.cash += self.revenue
        self.last_sales = units_sold

        if sales_rate > 0.85:
            self.price *= 1.01
            self.wage_offer *= 1.002
        elif sales_rate < 0.35:
            self.price *= 0.99
            self.wage_offer *= 0.998

        self.price = max(self.price, 0.1)
        self.wage_offer = max(self.wage_offer, 0.1)

        if self.cash < -10:
            self.active = False
            self.fire_all()

    def fire_all(self) -> None:
        for worker in self.workers:
            worker.employer = None
        self.workers.clear()
