import numpy as np
from typing import Dict, List, Optional
from scripts.sae.core import TreeOPOGroup

class AdaptiveSpectralSolver:
    """
    Dynamically interpolates between V_E(p) (O(N) heuristic) and the formal SAE QP projection
    based on the spectral radius of the parent-child adjacency matrix.
    """
    def __init__(self, tau_equilibrium: float = 0.12):
        self.tau_equilibrium = tau_equilibrium

    def compute_spectral_radius(self, group: TreeOPOGroup) -> float:
        """
        Computes the spectral radius rho(D_parent - D_children) as a proxy for structural non-stationarity.
        For simplicity in this harness, we construct the adjacency matrix from C_pair.
        """
        num_samples = len(group.samples)
        if num_samples == 0:
            return 0.0

        adj_matrix = np.zeros((num_samples, num_samples))
        for i, (p_i, _) in enumerate(group.samples):
            for j, (p_j, _) in enumerate(group.samples):
                if i != j and p_j.startswith(p_i) and p_i != p_j:
                    adj_matrix[i, j] = 1.0

        D_parent = np.diag(np.sum(adj_matrix, axis=1))
        D_children = np.diag(np.sum(adj_matrix, axis=0))
        laplacian = D_parent - D_children

        eigenvalues = np.linalg.eigvals(laplacian)
        return float(np.max(np.abs(eigenvalues))) if len(eigenvalues) > 0 else 0.0

    def compute_kl_divergence_proxy(self, group: TreeOPOGroup) -> float:
        """
        Mock implementation of D_KL(pi_student || pi_teacher).
        In a real system, this would be passed from the active training loop.
        We simulate it based on reward variance as a surrogate.
        """
        rewards = np.array([sample[1] for sample in group.samples])
        if len(rewards) < 2:
            return 0.0
        return float(np.var(rewards) + 0.05) # Add small epsilon

    def compute_psi(self, group: TreeOPOGroup) -> float:
        """
        Computes the Spectral Information Discrepancy metric (Psi).
        Psi = rho(D_parent - D_children) * D_KL(pi_student || pi_teacher)
        """
        rho = self.compute_spectral_radius(group)
        kl_div = self.compute_kl_divergence_proxy(group)
        return rho * kl_div

    def get_shannon_entropy(self, group: TreeOPOGroup) -> float:
        """
        Proxy for the local Shannon entropy of completion token distributions.
        """
        success_rate = sum(1 for _, r in group.samples if r > 0.5) / max(1, len(group.samples))
        if success_rate == 0 or success_rate == 1:
            return 0.0
        return -success_rate * np.log2(success_rate) - (1 - success_rate) * np.log2(1 - success_rate)

    def compute_advantages(self, group: TreeOPOGroup) -> np.ndarray:
        """
        Adaptive solver router based on Psi.
        """
        psi = self.compute_psi(group)

        if psi < self.tau_equilibrium:
            # Low non-stationarity: Use O(N) heuristic expectation baseline
            return group.compute_heuristic_advantages(alpha=0.5)
        else:
            # High non-stationarity: Use SLSQP with dynamically scaled margin
            entropy = self.get_shannon_entropy(group)
            dynamic_margin = 0.01 + (entropy * 0.05)
            return group.compute_sae_qp_advantages(margin=dynamic_margin, soft=True)
