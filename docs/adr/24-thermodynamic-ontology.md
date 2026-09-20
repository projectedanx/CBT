# 24. Thermodynamic Ontology of Computational Decision-Making

Date: 2024-05-20

## Status

Accepted

## Context

The system has recognized that pure logical abstraction of decision-making algorithms creates an engineering blind spot. Information is physical, and computational state changes carry a thermodynamic cost bounded by Landauer's Principle. The "Unified Energy Survival-Conversion Law" necessitates mapping algorithmic hoarding (search spaces) to explicit thermodynamic constraints to prevent catastrophic performance collapse in high-frequency constraints (like a 1.0s `actTimeout`).

To address this, three distinct systemic implementations have been created mapped to three cross-domain decision-making paradoxes:
1. **Kinematic MCTS and Reversible Tree Recycling:** Instead of discarding the MCTS tree via *tabula rasa* resetting (an irreversible erasure event), we implemented persistent tree recycling (`scripts/mcts_tree_recycling.py`). This limits Landauer erasure costs strictly to unchosen branches via Autophagic Pruning, conserving ancestral visitation mass.
2. **Constrained Convex ADMM Projection:** To maintain stable gradient scaling in Staged Advantage Estimation (SAE), a vectorized lock-free PyTorch implementation (`scripts/sae/admm_projector_pytorch.py`) was introduced. It dramatically outperforms traditional active-set SLSQP solvers by pre-factoring the DAG constraint matrix and operating in $O(N^2)$ time.
3. **Quantum Walk-Inspired State-Space Reduction (SSR):** To combat combinatorial state-space explosion, a Qiskit framework (`scripts/qw_ssr.py`) models search constraints as a discrete quantum random walk. An integrated phase oracle paired with QSVT amplitude amplification bypasses classical exponential scaling to return valid paths avoiding spatial hazards (e.g., Solar Exclusion Radii).

## Decision

We will integrate these three implementations as the core Thermodynamic Baseline of the agent architecture. Dependency pruning (`requirements.txt`) reflects standard boundaries to support Torch and Qiskit.

## Consequences

*   **Positive:** The system can now solve deep-ply ($\ge 20$-ply) MCTS rollouts well within the $1.0\text{s}$ limit by recycling states.
*   **Positive:** SAE optimization natively handles kinematic-economic coupling margins scaling quadratically in batches.
*   **Positive:** High-dimensionality trajectory checking can be pre-filtered algorithmically via the QW-SSR pattern.
*   **Negative:** Added complexity to dependency management and strict version pinning of PyTorch and Qiskit.
