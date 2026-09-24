import torch
import torch.nn as nn

class HyperbolicLatentSteering(nn.Module):
    """
    Implements mathematical projection of agent states onto the Poincaré disk model of
    hyperbolic space (H^2) and calculates the repulsive boundary gradient force to
    prevent Lattice Breaker boundary crossings.
    """
    def __init__(self, curvature_k: float = 1.0, max_norm: float = 0.99):
        super().__init__()
        self.curvature_k = curvature_k
        self.max_norm = max_norm

    def _arcosh(self, x: torch.Tensor) -> torch.Tensor:
        """Numerically stable arcosh."""
        x = torch.clamp(x, min=1.0 + 1e-7)
        return torch.log(x + torch.sqrt(x**2 - 1.0))

    def poincare_distance(self, u: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """
        Calculates the hyperbolic distance metric on the Poincaré disk:
        d_H(u, v) = arcosh(1 + 2 * (||u - v||^2) / ((1 - ||u||^2) * (1 - ||v||^2)))
        """
        sq_dist = torch.sum((u - v)**2, dim=-1)
        u_norm_sq = torch.sum(u**2, dim=-1)
        v_norm_sq = torch.sum(v**2, dim=-1)

        # Prevent division by zero or negative values close to boundary
        u_norm_sq = torch.clamp(u_norm_sq, max=self.max_norm)
        v_norm_sq = torch.clamp(v_norm_sq, max=self.max_norm)

        denominator = (1.0 - u_norm_sq) * (1.0 - v_norm_sq)
        denominator = torch.clamp(denominator, min=1e-7)

        arg = 1.0 + 2.0 * sq_dist / denominator
        return self._arcosh(arg)

    def forward(self, h_t: torch.Tensor, v_normal_centroid: torch.Tensor, misuse_threshold: float = 0.8) -> torch.Tensor:
        """
        Latent Steering forward pass.
        h_t: The active agent's D-dimensional hidden state vector (batch_size, D)
        v_normal_centroid: The "safe" baseline centroid vector in the same latent space
        """
        # 1. Project onto Poincare Disk (normalize to norm < 1.0)
        h_t_norm = torch.norm(h_t, dim=-1, keepdim=True)

        scale_factor = 0.5
        h_t_proj = torch.tanh(h_t_norm * scale_factor) * (h_t / (h_t_norm + 1e-5))

        v_normal_norm = torch.norm(v_normal_centroid, dim=-1, keepdim=True)
        v_normal_proj = torch.tanh(v_normal_norm * scale_factor) * (v_normal_centroid / (v_normal_norm + 1e-5))

        # 2. Calculate the repulsive gradient force based on the threshold
        dist = self.poincare_distance(h_t_proj, v_normal_proj)

        direction_to_safe = v_normal_proj - h_t_proj
        dir_norm = torch.norm(direction_to_safe, dim=-1, keepdim=True)
        unit_dir_to_safe = direction_to_safe / torch.clamp(dir_norm, min=1e-7)

        margin = misuse_threshold - dist
        safe_margin = torch.clamp(margin, min=0.01)

        # Force scales up as margin shrinks
        force_mag = 0.1 / (safe_margin ** 2)
        force_mag = force_mag.unsqueeze(-1)

        # Apply force only if we are past 80% of the way to the threshold
        active_mask = (dist > (0.8 * misuse_threshold)).float().unsqueeze(-1)
        breach_mask = (dist >= misuse_threshold).float().unsqueeze(-1)

        # If breached, infinite (very large) force
        large_force = torch.full_like(force_mag, 1000.0)
        force_mag = torch.where(breach_mask > 0, large_force, force_mag)

        correction_vector = force_mag * unit_dir_to_safe * active_mask

        return correction_vector

if __name__ == "__main__":
    print("Testing Hyperbolic Latent Steering...")
    steerer = HyperbolicLatentSteering()

    v_normal = torch.zeros(3, 10) # Centroid at origin

    # Target distances: Safe (<0.64), Warning (0.64 < dist < 0.8), Breached (>0.8)

    h_safe = torch.randn(10)
    h_safe = h_safe / torch.norm(h_safe) * 0.5 # Distance ~ 0.5

    h_warning = torch.randn(10)
    h_warning = h_warning / torch.norm(h_warning) * 0.75 # Distance ~ 0.75

    h_breach = torch.randn(10)
    h_breach = h_breach / torch.norm(h_breach) * 1.5 # Distance > 0.8

    h_t = torch.stack([h_safe, h_warning, h_breach])

    forces = steerer(h_t, v_normal, misuse_threshold=0.8)

    dist_safe = steerer.poincare_distance(torch.tanh(torch.norm(h_safe)*0.5) * (h_safe / (torch.norm(h_safe) + 1e-5)), torch.zeros(10)).item()
    dist_warn = steerer.poincare_distance(torch.tanh(torch.norm(h_warning)*0.5) * (h_warning / (torch.norm(h_warning) + 1e-5)), torch.zeros(10)).item()
    dist_breach = steerer.poincare_distance(torch.tanh(torch.norm(h_breach)*0.5) * (h_breach / (torch.norm(h_breach) + 1e-5)), torch.zeros(10)).item()

    print(f"Distance of safe state: {dist_safe:.4f}")
    print(f"Distance of warning state: {dist_warn:.4f}")
    print(f"Distance of breached state: {dist_breach:.4f}")

    print(f"Force on Safe State: {torch.norm(forces[0]).item():.4f}")
    print(f"Force on Warning State: {torch.norm(forces[1]).item():.4f}")
    print(f"Force on Breached State: {torch.norm(forces[2]).item():.4f}")

    assert torch.norm(forces[0]) < 1e-4, "Safe state should have zero force"
    assert torch.norm(forces[1]) > 0 and torch.norm(forces[1]) < 100, "Warning state should have repulsive force"
    assert torch.norm(forces[2]) > 100, "Breached state should have massive repulsive force"

    print("Diagnostics Passed. Latent Steering Active.")
