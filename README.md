# token-economics-calculator

Cheap tokens are an architectural assumption, not a law of nature.

This repo helps AI builders model cost per user action, caching savings, batch inference savings, break-even points, and what happens if token prices move 2x, 3x, or 5x.

## Calendar Note

The content plan marks W2 Friday, "Current LLM token prices are VC-subsidised," as the first linked post. The calendar CTA for W2 asks readers what their unit economics look like after a 3x token price increase, but it does not explicitly name this repo. Treat W2 as the concept launch unless that CTA is updated. Later calendar posts name this repo explicitly.

## Quickstart

```powershell
cd "D:\W6H\Github Content\token-economics-calculator"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .[dev]
python examples\therapy_bot_demo.py
python -m pytest
```

For non-coding readers, open:

```text
templates/Token_Economics_Template.xlsx
```

## What It Models

- current cost per action/session/user
- prompt caching savings
- batch inference savings
- break-even active users
- gross margin at scale
- 2x, 3x, and 5x token price shocks

## Python Example

```python
from calculator.cost_model import ModelPricing, UsagePattern, calculate_cost
from calculator.price_shock import simulate_price_shocks

pricing = ModelPricing("gpt-4.1-mini", input_per_million=0.40, output_per_million=1.60)
usage = UsagePattern(input_tokens=3200, output_tokens=900, requests_per_session=4, sessions_per_user=8)
cost = calculate_cost(pricing, usage)
print(cost.cost_per_session)
print(simulate_price_shocks(cost, revenue_per_session=1.20))
```

## Update Pricing

Provider pricing changes. Keep current assumptions in one place:

- Python: `calculator/pricing.py`
- Excel: `templates/Token_Economics_Template.xlsx`, `Pricing` sheet

The defaults are examples, not live pricing guarantees.

## Worked Therapy Bot Example

The included demo compares a launch configuration with an optimized configuration:

- fewer repeated system tokens through prompt caching
- model routing where only complex steps use expensive models
- batch processing for delayed summaries
- price shock table at 2x, 3x, and 5x

## Content Hooks

- "What happens to your AI product if token prices triple?"
- "Caching is margin protection."
- "Before building an AI product, model cost per user action."
- "Cost architecture is product strategy."
