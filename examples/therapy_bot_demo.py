from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from calculator.batch_inference import BatchScenario, compare_batch_inference
from calculator.breakeven import calculate_break_even
from calculator.caching_savings import CacheScenario, estimate_caching_savings
from calculator.cost_model import UsagePattern, calculate_cost
from calculator.price_shock import simulate_price_shocks
from calculator.pricing import DEFAULT_PRICING


def main() -> None:
    data = json.loads((ROOT / "examples" / "therapy_bot_cost_model.json").read_text(encoding="utf-8"))
    launch = data["launch"]
    optimized = data["optimized"]

    launch_cost = calculate_cost(
        DEFAULT_PRICING[launch["model"]],
        UsagePattern(
            launch["input_tokens"],
            launch["output_tokens"],
            launch["requests_per_session"],
            launch["sessions_per_user"],
        ),
    )
    optimized_cost = calculate_cost(
        DEFAULT_PRICING[optimized["model"]],
        UsagePattern(
            optimized["input_tokens"],
            optimized["output_tokens"],
            optimized["requests_per_session"],
            optimized["sessions_per_user"],
        ),
    )
    cache = estimate_caching_savings(
        DEFAULT_PRICING[optimized["model"]],
        UsagePattern(optimized["input_tokens"], optimized["output_tokens"], optimized["requests_per_session"], optimized["sessions_per_user"]),
        CacheScenario(**optimized["cache"]),
    )
    batch = compare_batch_inference(optimized_cost, BatchScenario(**optimized["batch"]))
    shocks = simulate_price_shocks(optimized_cost, revenue_per_session=data["revenue_per_session"])
    breakeven = calculate_break_even(
        revenue_per_user=data["revenue_per_session"] * optimized["sessions_per_user"],
        variable_cost_per_user=optimized_cost.cost_per_user,
        fixed_monthly_cost=5000,
        sessions_per_user=optimized["sessions_per_user"],
    )

    print("Token economics demo")
    print(f"launch session cost: ${launch_cost.cost_per_session:.4f}")
    print(f"optimized session cost: ${optimized_cost.cost_per_session:.4f}")
    print(f"cache optimized session cost: ${cache.optimized_session_cost:.4f}")
    print(f"batch optimized session cost: ${batch.optimized_session_cost:.4f}")
    print(f"break-even users at $5k fixed cost: {breakeven.break_even_users}")
    print("price shocks:")
    for shock in shocks:
        print(f"  {shock.multiplier:g}x -> ${shock.cost_per_session:.4f}, margin {shock.gross_margin_percent:.1%}, survives={shock.survives}")


if __name__ == "__main__":
    main()
