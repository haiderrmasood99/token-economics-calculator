from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class BreakEvenResult:
    contribution_margin_per_user: float
    break_even_users: int
    break_even_sessions: int
    monthly_gross_margin: float


def calculate_break_even(
    revenue_per_user: float,
    variable_cost_per_user: float,
    fixed_monthly_cost: float,
    sessions_per_user: int,
) -> BreakEvenResult:
    if sessions_per_user <= 0:
        raise ValueError("sessions_per_user must be positive")
    contribution = revenue_per_user - variable_cost_per_user
    if contribution <= 0:
        return BreakEvenResult(contribution, math.inf, math.inf, -fixed_monthly_cost)
    users = math.ceil(fixed_monthly_cost / contribution)
    return BreakEvenResult(
        contribution_margin_per_user=contribution,
        break_even_users=users,
        break_even_sessions=users * sessions_per_user,
        monthly_gross_margin=users * contribution - fixed_monthly_cost,
    )
