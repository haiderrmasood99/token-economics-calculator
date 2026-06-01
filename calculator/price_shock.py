from __future__ import annotations

from dataclasses import dataclass

from .cost_model import CostBreakdown


@dataclass(frozen=True)
class PriceShockResult:
    multiplier: float
    cost_per_session: float
    gross_margin_per_session: float
    gross_margin_percent: float
    survives: bool


def simulate_price_shocks(
    cost: CostBreakdown,
    revenue_per_session: float,
    multipliers: tuple[float, ...] = (1.0, 2.0, 3.0, 5.0),
    minimum_margin_percent: float = 0.30,
) -> list[PriceShockResult]:
    if revenue_per_session <= 0:
        raise ValueError("revenue_per_session must be positive")
    results: list[PriceShockResult] = []
    for multiplier in multipliers:
        shocked_cost = cost.cost_per_session * multiplier
        margin = revenue_per_session - shocked_cost
        margin_percent = margin / revenue_per_session
        results.append(
            PriceShockResult(
                multiplier=multiplier,
                cost_per_session=shocked_cost,
                gross_margin_per_session=margin,
                gross_margin_percent=margin_percent,
                survives=margin_percent >= minimum_margin_percent,
            )
        )
    return results
