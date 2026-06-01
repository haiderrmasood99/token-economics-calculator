from calculator.batch_inference import BatchScenario, compare_batch_inference
from calculator.breakeven import calculate_break_even
from calculator.caching_savings import CacheScenario, estimate_caching_savings
from calculator.cost_model import ModelPricing, UsagePattern, calculate_cost


def test_calculate_cost_per_session() -> None:
    pricing = ModelPricing("example", input_per_million=1.0, output_per_million=2.0)
    usage = UsagePattern(input_tokens=1000, output_tokens=500, requests_per_session=10, sessions_per_user=4)

    cost = calculate_cost(pricing, usage)

    assert round(cost.cost_per_request, 6) == 0.002
    assert round(cost.cost_per_session, 6) == 0.02
    assert round(cost.cost_per_user, 6) == 0.08


def test_caching_savings_reduces_session_cost() -> None:
    pricing = ModelPricing("example", input_per_million=1.0, output_per_million=2.0)
    usage = UsagePattern(input_tokens=10_000, output_tokens=1_000, requests_per_session=2)

    result = estimate_caching_savings(pricing, usage, CacheScenario(0.5, 0.8, 0.5))

    assert result.optimized_session_cost < result.baseline_session_cost
    assert result.savings_percent > 0


def test_batch_inference_reduces_batchable_share() -> None:
    cost = calculate_cost(ModelPricing("example", 1, 1), UsagePattern(1000, 1000, 10))

    result = compare_batch_inference(cost, BatchScenario(batchable_request_share=0.5, batch_discount=0.5))

    assert result.optimized_session_cost == cost.cost_per_session * 0.75


def test_break_even_users() -> None:
    result = calculate_break_even(revenue_per_user=20, variable_cost_per_user=5, fixed_monthly_cost=150, sessions_per_user=10)

    assert result.break_even_users == 10
    assert result.break_even_sessions == 100
