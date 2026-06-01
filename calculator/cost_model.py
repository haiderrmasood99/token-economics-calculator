from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPricing:
    model_name: str
    input_per_million: float
    output_per_million: float


@dataclass(frozen=True)
class UsagePattern:
    input_tokens: int
    output_tokens: int
    requests_per_session: int
    sessions_per_user: int = 1


@dataclass(frozen=True)
class CostBreakdown:
    model_name: str
    cost_per_request: float
    cost_per_session: float
    cost_per_user: float
    input_cost_per_request: float
    output_cost_per_request: float


def calculate_cost(pricing: ModelPricing, usage: UsagePattern) -> CostBreakdown:
    _validate(pricing, usage)
    input_cost = usage.input_tokens / 1_000_000 * pricing.input_per_million
    output_cost = usage.output_tokens / 1_000_000 * pricing.output_per_million
    per_request = input_cost + output_cost
    per_session = per_request * usage.requests_per_session
    return CostBreakdown(
        model_name=pricing.model_name,
        cost_per_request=per_request,
        cost_per_session=per_session,
        cost_per_user=per_session * usage.sessions_per_user,
        input_cost_per_request=input_cost,
        output_cost_per_request=output_cost,
    )


def _validate(pricing: ModelPricing, usage: UsagePattern) -> None:
    values = [
        pricing.input_per_million,
        pricing.output_per_million,
        usage.input_tokens,
        usage.output_tokens,
        usage.requests_per_session,
        usage.sessions_per_user,
    ]
    if any(value < 0 for value in values):
        raise ValueError("pricing and usage values must be non-negative")
    if usage.requests_per_session == 0:
        raise ValueError("requests_per_session must be positive")
