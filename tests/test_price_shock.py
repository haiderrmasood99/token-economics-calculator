from calculator.cost_model import ModelPricing, UsagePattern, calculate_cost
from calculator.price_shock import simulate_price_shocks


def test_price_shock_marks_survival_against_margin_threshold() -> None:
    cost = calculate_cost(ModelPricing("example", 1.0, 1.0), UsagePattern(10_000, 10_000, 10))

    shocks = simulate_price_shocks(cost, revenue_per_session=1.0, multipliers=(1, 3, 5), minimum_margin_percent=0.5)

    assert shocks[0].survives is True
    assert shocks[-1].cost_per_session == cost.cost_per_session * 5
    assert shocks[-1].gross_margin_percent < shocks[0].gross_margin_percent
