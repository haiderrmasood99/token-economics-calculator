# token-economics-calculator

Token cost is part of product architecture.

This repository helps you estimate how much an LLM-powered feature costs to run, how that cost changes at scale, and how much margin you can protect with caching, batching, and better model choices. It includes both Python code for engineers and an Excel workbook for founders, operators, and product teams who prefer spreadsheets.

The examples use made-up numbers. Always check current provider pricing before using the results for a real business decision.

## What You Can Calculate

- Cost per request, session, user, and month.
- Prompt caching savings.
- Batch inference savings for delayed jobs.
- Break-even user counts.
- Gross margin under different pricing assumptions.
- Price shock scenarios at 2x, 3x, and 5x token prices.

## Project Structure

```text
.
|-- calculator/
|   |-- cost_model.py          # Core token cost model
|   |-- caching_savings.py     # Prompt caching savings
|   |-- batch_inference.py     # Batch inference cost comparison
|   |-- breakeven.py           # Break-even helper
|   |-- price_shock.py         # 2x, 3x, and 5x price scenarios
|   `-- pricing.py             # Example model pricing assumptions
|-- examples/
|   |-- therapy_bot_cost_model.json
|   `-- therapy_bot_demo.py
|-- templates/
|   `-- Token_Economics_Template.xlsx
|-- tests/
|-- pyproject.toml
`-- README.md
```

## Quickstart

Clone the repository:

```bash
git clone https://github.com/haiderrmasood99/token-economics-calculator.git
cd token-economics-calculator
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the package with test dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the demo:

```bash
python examples/therapy_bot_demo.py
```

Run the tests:

```bash
python -m pytest
```

## Spreadsheet Option

If you do not want to run Python, open:

```text
templates/Token_Economics_Template.xlsx
```

The workbook mirrors the Python model. Use it to change token volumes, model prices, request counts, revenue, and expected cache hit rates.

## Basic Python Example

```python
from calculator.cost_model import ModelPricing, UsagePattern, calculate_cost
from calculator.price_shock import simulate_price_shocks

pricing = ModelPricing(
    model_name="example-mini-model",
    input_per_million=0.40,
    output_per_million=1.60,
)

usage = UsagePattern(
    input_tokens=3200,
    output_tokens=900,
    requests_per_session=4,
    sessions_per_user=8,
)

cost = calculate_cost(pricing, usage)
print(cost.cost_per_session)

shock_table = simulate_price_shocks(cost, revenue_per_session=1.20)
for row in shock_table:
    print(row)
```

## Worked Example

The included demo compares a simple launch setup against a more cost-aware setup for a therapy-style assistant.

It shows:

- The cost of a repeated conversation flow.
- Savings from prompt caching.
- Savings from batch processing delayed summaries.
- How the same feature behaves if token prices increase.
- How many users are needed to cover fixed monthly costs.

Run it with:

```bash
python examples/therapy_bot_demo.py
```

## Updating Model Prices

Provider prices change. Keep your assumptions in one place:

- Python: `calculator/pricing.py`
- Excel: `templates/Token_Economics_Template.xlsx`, `Pricing` sheet

Before using this calculator for a real product, update those values from the current provider pricing pages.

## How To Read The Results

Start with cost per session. That number is easier to reason about than cost per token.

Then compare it to revenue per session or expected revenue per user. If the margin only works with today's cheapest possible pricing, the product may be fragile. Caching, batching, model routing, shorter prompts, and better context management are not just optimizations. They can decide whether the product works as a business.

## Notes

- No API keys are required.
- No network calls are made by the demo.
- All examples are synthetic.
- The calculator is an educational planning tool, not financial advice.
