from __future__ import annotations

from dataclasses import dataclass

from .cost_model import ModelPricing, UsagePattern, calculate_cost


@dataclass(frozen=True)
class CacheScenario:
    reusable_input_token_share: float
    cache_hit_rate: float
    cached_input_discount: float


@dataclass(frozen=True)
class CacheSavingsResult:
    baseline_session_cost: float
    optimized_session_cost: float
    savings_per_session: float
    savings_percent: float


def estimate_caching_savings(pricing: ModelPricing, usage: UsagePattern, scenario: CacheScenario) -> CacheSavingsResult:
    _validate_share(scenario.reusable_input_token_share, "reusable_input_token_share")
    _validate_share(scenario.cache_hit_rate, "cache_hit_rate")
    _validate_share(scenario.cached_input_discount, "cached_input_discount")

    baseline = calculate_cost(pricing, usage)
    cached_tokens = usage.input_tokens * scenario.reusable_input_token_share * scenario.cache_hit_rate
    full_price_tokens = usage.input_tokens - cached_tokens
    discounted_input_cost = (
        full_price_tokens / 1_000_000 * pricing.input_per_million
        + cached_tokens / 1_000_000 * pricing.input_per_million * (1 - scenario.cached_input_discount)
    )
    output_cost = usage.output_tokens / 1_000_000 * pricing.output_per_million
    optimized_session = (discounted_input_cost + output_cost) * usage.requests_per_session
    savings = baseline.cost_per_session - optimized_session
    return CacheSavingsResult(
        baseline_session_cost=baseline.cost_per_session,
        optimized_session_cost=optimized_session,
        savings_per_session=savings,
        savings_percent=savings / baseline.cost_per_session if baseline.cost_per_session else 0.0,
    )


def _validate_share(value: float, name: str) -> None:
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")
