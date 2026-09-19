import numpy as np
from typing import Dict, Tuple
from scripts.sae.core import TreeOPOGroup

class EWARHarness:
    """
    Entropy-Weighted Advantage Recovery (EWAR) hook inside the loss calculation.
    Analyzes, detects, and mitigates "Semantic Saponification" (advantage variance collapse).
    """
    def __init__(self, variance_threshold: float = 0.05, corr_threshold: float = 0.1):
        self.variance_threshold = variance_threshold
        self.corr_threshold = corr_threshold
        self.saponification_active = False

    def compute_saponification_correlation(self, group: TreeOPOGroup, advantages: np.ndarray, action_value_partials: np.ndarray) -> float:
        """
        Calculates chi: the correlation between advantage magnitude |a*| and the
        mixed partial derivative of the action value.
        """
        if len(advantages) < 2 or len(action_value_partials) < 2:
            return 1.0 # Safe default

        adv_mag = np.abs(advantages)

        # Check for zero variance to avoid division by zero
        if np.var(adv_mag) == 0 or np.var(action_value_partials) == 0:
            return 0.0

        corr_matrix = np.corrcoef(adv_mag, action_value_partials)
        return float(corr_matrix[0, 1])

    def detect_collapse(self, group: TreeOPOGroup, advantages: np.ndarray, action_value_partials: np.ndarray) -> bool:
        """
        Monitors advantage variance across the prefix tree.
        If chi -> 0 and accuracy plateaus (simulated here by variance threshold), trigger EWAR.
        """
        chi = self.compute_saponification_correlation(group, advantages, action_value_partials)
        adv_var = np.var(advantages)

        if np.isnan(chi):
            chi = 0.0

        if abs(chi) < self.corr_threshold or adv_var < self.variance_threshold:
            self.saponification_active = True
        else:
            self.saponification_active = False

        return self.saponification_active

    def apply_ewar_hook(self, group: TreeOPOGroup, base_advantages: np.ndarray, prefix_log_probs: Dict[str, float]) -> np.ndarray:
        """
        Active Entropy-Weighted Advantage Recovery hook.
        Overrides standard normalization, forces c=1, and scales advantages by the
        inverse log-probability of the parent prefix to restore structural contrast.
        """
        if not self.saponification_active:
            return base_advantages

        recovered_advantages = np.zeros_like(base_advantages)

        for i, (prefix_id, _) in enumerate(group.samples):
            # Fetch log prob of parent (or default if root)
            node = group.nodes.get(prefix_id)
            parent_log_prob = -1.0 # Default fallback

            if node and node.parent_id and node.parent_id in prefix_log_probs:
                parent_log_prob = prefix_log_probs[node.parent_id]

            # Avoid division by zero, scale by inverse log-prob magnitude
            inv_scale = 1.0 / (abs(parent_log_prob) + 1e-5)

            # Apply scaling
            recovered_advantages[i] = base_advantages[i] * inv_scale

        # First mean-center to maintain zero-mean invariant
        recovered_advantages = recovered_advantages - np.mean(recovered_advantages)

        # Force L2 norm = N (c=1 scale preservation)
        n = len(recovered_advantages)
        norm_sq = np.dot(recovered_advantages, recovered_advantages)

        if norm_sq > 0:
            recovered_advantages = recovered_advantages * np.sqrt(n / norm_sq)

        return recovered_advantages
