import torch
import numpy as np
from typing import Tuple, List, Optional
from scripts.sae.core import TreeOPOGroup

class PyTorchADMMProjector:
    """
    Lock-free, vectorized PyTorch implementation of the Alternating Direction Method of Multipliers (ADMM)
    solver for the Staged Advantage Estimation (SAE) convex projection, incorporating kinematic-economic constraints.
    """
    def __init__(self, group: TreeOPOGroup, rho: float = 1.0, max_iter: int = 100, tol: float = 1e-6, device: str = 'cpu'):
        self.group = group
        self.rho = rho
        self.max_iter = max_iter
        self.tol = tol
        self.device = torch.device(device)
        self.active_advantages = None

    def _kinematic_margin(self, m: float) -> float:
        """
        Calculates penalty margin based on non-linear kinematic-economic coupling.
        v(m) = 1 + 5(ln m / ln 1000)^1.5
        """
        # Constrain minimum mass to avoid domain error
        m = max(1.0, m)
        v = 1.0 + 5.0 * (np.log(m) / np.log(1000.0)) ** 1.5
        return float(v * 0.01) # scale base margin by velocity

    def _build_L_matrix(self, default_margin: float = 0.01) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Builds the constraint matrix L and vector b (L*a <= b) mapping parent-child and triplet DAG ordering.
        Incorporates dynamic penalty margins derived from kinematic scaling constraints.
        """
        num_samples = len(self.group.samples)
        # Fallback empty constraints
        if num_samples == 0:
            return torch.zeros((0, 0), device=self.device), torch.zeros(0, device=self.device)

        constraints = self.group.build_ordering_constraints(default_margin)
        num_constraints = len(constraints)

        if num_constraints == 0:
            return torch.zeros((0, num_samples), device=self.device), torch.zeros(0, device=self.device)

        L = torch.zeros((num_constraints, num_samples), dtype=torch.float64, device=self.device)
        b = torch.zeros(num_constraints, dtype=torch.float64, device=self.device)

        for idx, (i, j, margin) in enumerate(constraints):
            # i and j relations derived from Core implementation
            # a_i + delta <= a_j  -> a_i - a_j <= -delta
            # However we want dynamic delta:
            # Emulate mass derived from reward score purely for demonstration scaling.
            # In actual production mass would be drawn from node metadata.
            pseudo_mass = max(10.0, 100.0 * abs(self.group.samples[i][1]))
            dyn_margin = self._kinematic_margin(pseudo_mass)

            # Solar exclusion zone penalty modifier
            # Using placeholder (50, 50, R=10.0) mapping; assuming trajectory violation adds strict penalty.
            if abs(self.group.samples[i][1]) < 0.2: # Proxy for trajectory violation
                 dyn_margin += 0.5

            L[idx, i] = 1.0
            L[idx, j] = -1.0
            b[idx] = -dyn_margin

        return L, b

    def _project_l2_ball(self, v: torch.Tensor, radius_sq: float) -> torch.Tensor:
        """
        Vectorized PyTorch analytical projection onto the L2-ball ||a||_2^2 <= N.
        """
        norm_sq = torch.dot(v, v)
        if norm_sq <= radius_sq:
            return v
        return v * torch.sqrt(radius_sq / norm_sq)

    def solve(self, r_0: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Executes the ADMM core loop using PyTorch tensor operations.
        Minimizes 0.5 * ||a - r_0||^2 subject to L*a <= b, sum(a) = 0, and ||a||^2 <= N.
        """
        if r_0 is None:
            rewards = np.array([sample[1] for sample in self.group.samples], dtype=np.float64)
            if len(rewards) == 0:
                return np.array([])
            r_0 = rewards - np.mean(rewards)

        n = len(r_0)

        # Move to Torch tensor space
        r_0_t = torch.tensor(r_0, dtype=torch.float64, device=self.device)

        L, b = self._build_L_matrix()
        m_constraints = L.shape[0]

        a = r_0_t.clone()
        z = torch.zeros(m_constraints, dtype=torch.float64, device=self.device)
        u = torch.zeros(m_constraints, dtype=torch.float64, device=self.device)

        if m_constraints == 0:
            a_centered = a - torch.mean(a)
            final_a = self._project_l2_ball(a_centered, float(n))
            self.active_advantages = final_a.cpu().numpy()
            return self.active_advantages

        # Matrix pre-factorization: inv(I + rho * L^T * L)
        I = torch.eye(n, dtype=torch.float64, device=self.device)
        L_t_L = torch.matmul(L.t(), L)
        inv_matrix = torch.inverse(I + self.rho * L_t_L)

        for _ in range(self.max_iter):
            # 1. a-update
            rhs = r_0_t + self.rho * torch.matmul(L.t(), b - z + u)
            a_new = torch.matmul(inv_matrix, rhs)

            # Enforce mean(a) = 0
            a_new = a_new - torch.mean(a_new)

            # Enforce L2 norm bound ||a||^2 <= N
            a_new = self._project_l2_ball(a_new, float(n))

            # 2. z-update
            La = torch.matmul(L, a_new)
            z_new = torch.maximum(torch.zeros_like(b), b - La + u)

            # 3. u-update
            u_new = u + b - La - z_new

            # Convergence Check
            primal_res = torch.norm(b - La - z_new)
            dual_res = torch.norm(self.rho * torch.matmul(L.t(), z_new - z))

            a = a_new
            z = z_new
            u = u_new

            if primal_res < self.tol and dual_res < self.tol:
                break

        self.active_advantages = a.cpu().numpy()
        return self.active_advantages
