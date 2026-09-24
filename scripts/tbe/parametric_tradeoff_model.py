"""
Parametric Trade-off Model for the Temporal Blending Engine (TBE).
Models the Tension Frontier between Creativity (Novelty) and Coherence (Grounding),
adjusting CFDI thresholds based on CCH (Cost of Coherence) and CSD (Cost of Structural Discovery).
"""

from typing import Dict, Any

class ParametricTradeoffModel:
    """
    Dynamically balances the Cost of Coherence Overhead (CCH) against
    the Cost of Structural Discovery (CSD).
    """

    def __init__(self, base_csd_budget: float = 100.0, base_cpi_threshold: float = 0.95):
        self.base_csd_budget = base_csd_budget
        self.base_cpi_threshold = base_cpi_threshold

    def calculate_cch(self, verification_depth: int, tokens: int) -> float:
        """
        Calculates Cost of Coherence Overhead (CCH).
        CCH is proportional to Verification Depth * Tokens.
        """
        # Using an arbitrary constant for proportionality
        return 0.05 * verification_depth * tokens

    def calculate_csd(self, temperature: float, variance: float) -> float:
        """
        Calculates Cost of Structural Discovery (CSD).
        CSD is proportional to Temperature * Variance.
        """
        # Using an arbitrary constant for proportionality
        return 10.0 * temperature * variance

    def evaluate_optimality_frontier(self, current_cpi: float, csd: float) -> Dict[str, Any]:
        """
        Evaluates the trade-off frontier.
        If CPI >= 0.95, implies CSD <= Budget. If CSD is over-allocated,
        triggers high CFDI and locks output in Epistemic Escrow.
        """
        is_coherent = current_cpi >= self.base_cpi_threshold
        csd_within_budget = csd <= self.base_csd_budget

        status = "OPTIMAL"
        if not is_coherent:
            status = "COHERENCE_FAILURE"
        elif not csd_within_budget:
            status = "EPISTEMIC_ESCROW"  # Over-allocated CSD drops viscosity, triggers escrow

        return {
            "status": status,
            "cpi_coherent": is_coherent,
            "csd_within_budget": csd_within_budget,
            "current_csd": csd,
            "budget": self.base_csd_budget
        }

    def calculate_dynamic_cfdi_threshold(self, cch: float, csd: float) -> float:
        """
        Dynamically tunes the Confidence-Fidelity Divergence Index (CFDI) threshold.
        Higher CSD (more discovery) requires tighter CFDI bounds to prevent drift,
        unless offset by extremely high CCH (deep verification).
        """
        # Base CFDI threshold is 0.42 (from architectural context)
        base_cfdi = 0.42

        # Ratio of Discovery to Verification
        ratio = csd / (cch + 1e-6)

        # If discovery heavily outweighs verification, tighten the threshold (lower is stricter)
        # If verification is heavy, we can afford slightly looser initial discovery thresholds
        adjustment = 0.1 * math.log(ratio + 0.1) if ratio > 0 else 0

        dynamic_threshold = base_cfdi - adjustment

        # Clamp to reasonable bounds [0.1, 0.8]
        return max(0.1, min(0.8, dynamic_threshold))

import math
