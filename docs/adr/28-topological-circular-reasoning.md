# ADR 28: Topological Detection of Circular Reasoning via Zigzag Persistent Homology

## Status
Accepted

## Context
In our multi-agent architecture (e.g., N2E-CED loops), agents frequently fall into circular reasoning patterns where they mutually reinforce biased or contradictory assumptions. This phenomenon, formalized as "Algorithmic Shame," breaks down logical coherence but cannot be reliably caught by simple semantic similarity metrics because the agents confidently output plausible-sounding prose.

## Decision
We will model the evolving multi-agent belief state as a dynamic point cloud in high-dimensional latent space. We integrate a **Chrono-Topological Governance Agent (CTGA)** to apply **Zigzag Persistent Homology** (using Vietoris-Rips filtrations) over these point clouds across dialogue turns.

*   We monitor **Betti-0 ($\beta_0$)** features to ensure Structural Conservation (preventing concept conflation).
*   We monitor **Betti-1 ($\beta_1$)** loops to detect Relational Contradictions and circular logic.
*   A highly persistent $\beta_1$ loop exceeding the threshold $\tau_p$ is classified as a **Symbolic Scar**.
*   Upon detection, the system triggers Epistemic Escrow and activates a **Reflexive Therapeutic Architecture (RTA)** using paraconsistent logic (Logic of Formal Inconsistency) to resolve the contradiction.

## Consequences
### Positive
*   Provides a rigorous, geometric, and verifiable mechanism for detecting complex logical fallacies that bypass standard semantic checks.
*   Enables the calculation of the **Symbolic Scar Softening Index (SSI)** to quantitatively prove that a contradiction has been resolved.

### Negative
*   **Computational Overhead (CCH):** Computing persistent homology scales cubically ($O(m^3)$). To mitigate this, we will use a Tiered Auditing Protocol: continuous low-resolution scans triggering targeted high-resolution local TDA audits only when anomalies are flagged.
