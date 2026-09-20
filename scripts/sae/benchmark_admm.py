import time
import numpy as np
import torch
from scripts.sae.core import TreeOPOGroup
from scripts.sae.admm_projector import ADMMProjector
from scripts.sae.admm_projector_pytorch import PyTorchADMMProjector

def generate_synthetic_group(batch_size: int) -> TreeOPOGroup:
    """Generates synthetic tree ordering data to benchmark quadratic scaling capabilities."""
    group = TreeOPOGroup("benchmark_group")
    # Build linear hierarchy
    group.add_node("root", None)
    for i in range(1, batch_size):
        prefix_id = f"prefix_{i}"
        parent_id = f"prefix_{i//2}" if i > 1 else "root"
        group.add_node(prefix_id, parent_id)

        # Map sample to node
        reward = np.random.uniform(0.0, 1.0)
        group.register_sample(prefix_id, reward)

    return group

def run_benchmarks():
    print("=========================================================")
    print(" ADMM SAE Projector Quadratic Scaling Benchmark")
    print("=========================================================")
    print(f"{'Batch (N)':<10} | {'SLSQP Baseline':<18} | {'PyTorch ADMM (ms)':<18}")
    print("-" * 55)

    batch_sizes = [16, 64, 256, 512, 1024]

    # Determine device availability
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    for N in batch_sizes:
        group = generate_synthetic_group(N)

        # 1. Baseline SLSQP Timing
        start_slsqp = time.perf_counter()
        try:
            # We enforce hard constraint resolution time limit fallback on SLSQP
            _ = group.compute_sae_qp_advantages()
            slsqp_ms = (time.perf_counter() - start_slsqp) * 1000
        except Exception:
            slsqp_ms = float('inf')

        # 2. PyTorch ADMM Timing
        pt_admm = PyTorchADMMProjector(group, device=device)
        start_pt = time.perf_counter()
        pt_advs = pt_admm.solve()
        pt_ms = (time.perf_counter() - start_pt) * 1000

        # Verification constraints
        mean_pt = np.mean(pt_advs)
        norm_sq = np.dot(pt_advs, pt_advs)
        primal_dual_epsilon = abs(mean_pt)

        print(f"{N:<10} | {slsqp_ms:>13.2f} ms | {pt_ms:>13.2f} ms")

        # Validate primal feasibility constraint (mean == 0)
        assert primal_dual_epsilon < 1e-5, f"Primal feasibility failed! Mean: {mean_pt}"

if __name__ == "__main__":
    run_benchmarks()
