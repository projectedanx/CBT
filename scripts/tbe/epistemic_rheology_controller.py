"""
Epistemic Rheology Controller for the Temporal Blending Engine (TBE).
Enforces Lipschitz continuity bounds on continuous latent semantic trajectories
to mathematically prevent Chronotopological Drift.
"""

import math
from typing import Dict, Any, Tuple

class EpistemicRheologyController:
    """
    Models the semantic flow as a viscous fluid to guarantee that the projected
    trace remains within the reachable set of safe causal states.
    """

    def __init__(self, semantic_viscosity: float = 1.0, quantization_resolution: float = 0.5):
        """
        Args:
            semantic_viscosity (float): Mu (mu) - Resistance of a concept to change.
            quantization_resolution (float): Delta (delta) - Spatial resolution of quantization operator.
        """
        self.mu = semantic_viscosity
        self.delta = quantization_resolution

    def calculate_lipschitz_bound(self, constraint_force_magnitude: float) -> float:
        """
        Calculates the Lipschitz constant L based on the constraint force and viscosity.
        L = ||f_constraint|| / mu
        """
        if self.mu <= 0:
            raise ValueError("Semantic viscosity (mu) must be > 0")
        return constraint_force_magnitude / self.mu

    def validate_step(self, constraint_force_magnitude: float, delta_t: float) -> Dict[str, Any]:
        """
        Validates if a temporal step size (delta_t) satisfies the rheological stability bound
        to prevent discontinuous Chronotopological Drift.
        """
        try:
            L = self.calculate_lipschitz_bound(constraint_force_magnitude)
        except ValueError as e:
            return {"valid": False, "reason": str(e)}

        max_displacement = L * delta_t
        is_stable = max_displacement < self.delta

        return {
            "valid": is_stable,
            "max_displacement": max_displacement,
            "allowed_delta": self.delta,
            "L_constant": L,
            "reason": "Stable Step" if is_stable else "Chronotopological Drift Detected (Lipschitz bound exceeded)"
        }

    def adjust_viscosity_for_stability(self, constraint_force_magnitude: float, delta_t: float) -> float:
        """
        Dynamically adjusts semantic viscosity (mu) to guarantee stability for a given step.
        Returns the minimum mu required.
        """
        # delta_t < delta / L => L < delta / delta_t => f / mu < delta / delta_t => mu > f * delta_t / delta
        min_required_mu = (constraint_force_magnitude * delta_t) / self.delta

        # Add a tiny epsilon to strictly satisfy the inequality
        epsilon = 1e-6
        return max(self.mu, min_required_mu + epsilon)
