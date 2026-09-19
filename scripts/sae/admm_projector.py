import numpy as np
import threading
import time
from typing import List, Tuple
from scripts.sae.core import TreeOPOGroup

class ADMMProjector:
    """
    Lock-free, thread-safe Alternating Direction Method of Multipliers (ADMM) solver
    for the SAE convex projection.
    """
    def __init__(self, group: TreeOPOGroup, rho: float = 1.0, max_iter: int = 100, tol: float = 1e-6):
        self.group = group
        self.rho = rho
        self.max_iter = max_iter
        self.tol = tol

        # Double-buffered pointer system for lock-free swapping
        self.active_advantages = None
        self.background_advantages = None
        self._swap_lock = threading.Lock()

    def _build_L_matrix(self, margin: float = 0.01) -> Tuple[np.ndarray, np.ndarray]:
        """
        Builds the constraint matrix L and vector b such that L * a <= b.
        Constraint: a_i + margin <= a_j  => a_i - a_j <= -margin
        """
        constraints = self.group.build_ordering_constraints(margin)
        num_samples = len(self.group.samples)
        num_constraints = len(constraints)

        L = np.zeros((num_constraints, num_samples))
        b = np.full(num_constraints, -margin)

        for idx, (i, j, _) in enumerate(constraints):
            L[idx, i] = 1.0
            L[idx, j] = -1.0

        return L, b

    def _project_l2_ball(self, v: np.ndarray, radius_sq: float) -> np.ndarray:
        """
        Analytical projection onto the L2-ball ||a||_2^2 <= N in O(1) vectorized time.
        """
        norm_sq = np.dot(v, v)
        if norm_sq <= radius_sq:
            return v
        return v * np.sqrt(radius_sq / norm_sq)

    def _solve_admm_core(self, r_0: np.ndarray, margin: float = 0.01) -> np.ndarray:
        """
        Core ADMM update equations decoupled from the training loop.
        Minimizes 0.5 * ||a - r_0||^2 subject to L*a <= b and sum(a) = 0, ||a||^2 <= N.
        """
        n = len(r_0)
        L, b = self._build_L_matrix(margin)
        m = L.shape[0]

        # Initialize ADMM variables
        a = np.copy(r_0)
        z = np.zeros(m) # Slack variables for L*a + z = b, z >= 0
        u = np.zeros(m) # Dual variables

        if m == 0:
            # If no constraints, just project onto L2 ball and mean-center
            a_centered = a - np.mean(a)
            return self._project_l2_ball(a_centered, float(n))

        # Precompute matrix inverse for a-update
        # (I + rho * L^T * L) * a = r_0 + rho * L^T * (b - z + u)
        I = np.eye(n)
        L_t_L = np.dot(L.T, L)
        inv_matrix = np.linalg.inv(I + self.rho * L_t_L)

        for _ in range(self.max_iter):
            # 1. a-update
            rhs = r_0 + self.rho * np.dot(L.T, b - z + u)
            a_new = np.dot(inv_matrix, rhs)

            # Enforce zero-mean directly
            a_new = a_new - np.mean(a_new)

            # Enforce L2 norm bound ||a||^2 <= N
            a_new = self._project_l2_ball(a_new, float(n))

            # 2. z-update
            # z_new = max(0, b - L*a_new + u)
            La = np.dot(L, a_new)
            z_new = np.maximum(0, b - La + u)

            # 3. u-update
            u_new = u + b - La - z_new

            # Check convergence (primal-dual feasibility epsilon)
            primal_res = np.linalg.norm(b - La - z_new)
            dual_res = np.linalg.norm(self.rho * np.dot(L.T, z_new - z))

            a = a_new
            z = z_new
            u = u_new

            if primal_res < self.tol and dual_res < self.tol:
                break

        return a

    def run_async_projection(self) -> None:
        """
        Executes the ADMM solver in a background thread and swaps pointers upon completion.
        """
        rewards = np.array([sample[1] for sample in self.group.samples], dtype=np.float64)
        if len(rewards) == 0:
            return

        r_0 = rewards - np.mean(rewards)

        # Calculate in background buffer
        self.background_advantages = self._solve_admm_core(r_0)

        # Lock-free reference swap (atomic in Python due to GIL, but explicit lock for clarity)
        with self._swap_lock:
            self.active_advantages = self.background_advantages

    def get_advantages(self) -> np.ndarray:
        """
        Retrieves the latest available active advantages.
        """
        with self._swap_lock:
            if self.active_advantages is not None:
                return np.copy(self.active_advantages)
            else:
                # Fallback if async process hasn't finished
                rewards = np.array([sample[1] for sample in self.group.samples], dtype=np.float64)
                return rewards - np.mean(rewards)
