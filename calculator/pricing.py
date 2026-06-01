from __future__ import annotations

from .cost_model import ModelPricing


DEFAULT_PRICING = {
    "gpt-4.1-mini": ModelPricing("gpt-4.1-mini", input_per_million=0.40, output_per_million=1.60),
    "gpt-4.1": ModelPricing("gpt-4.1", input_per_million=2.00, output_per_million=8.00),
    "claude-sonnet-example": ModelPricing("claude-sonnet-example", input_per_million=3.00, output_per_million=15.00),
}
