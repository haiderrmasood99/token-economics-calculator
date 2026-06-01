from __future__ import annotations

from dataclasses import dataclass

from .cost_model import CostBreakdown


@dataclass(frozen=True)
class BatchScenario:
    batchable_request_share: float
    batch_discount: float


@dataclass(frozen=True)
class BatchSavingsResult:
    baseline_session_cost: float
    optimized_session_cost: float
    savings_per_session: float
    savings_percent: float


def compare_batch_inference(cost: CostBreakdown, scenario: BatchScenario) -> BatchSavingsResult:
    if not 0 <= scenario.batchable_request_share <= 1:
        raise ValueError("batchable_request_share must be between 0 and 1")
    if not 0 <= scenario.batch_discount <= 1:
        raise ValueError("batch_discount must be between 0 and 1")
    discountable = cost.cost_per_session * scenario.batchable_request_share
    optimized = cost.cost_per_session - discountable * scenario.batch_discount
    savings = cost.cost_per_session - optimized
    return BatchSavingsResult(cost.cost_per_session, optimized, savings, savings / cost.cost_per_session if cost.cost_per_session else 0.0)
